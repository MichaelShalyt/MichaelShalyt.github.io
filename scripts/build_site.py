"""Build a static GitHub Pages site directly from the local WordPress export."""

from __future__ import annotations

import html
import json
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs
from urllib.parse import urlparse

# ROOT_DIRECTORY stores the repository root used for generated output.
ROOT_DIRECTORY = Path(__file__).resolve().parents[1]

# sys.path is extended so the build script can be run directly from the repository root.
sys.path.insert(0, str(ROOT_DIRECTORY))

from content.site_content import EXPORT_DIRECTORY
from content.site_content import MEDIA_LIBRARY_DIRECTORY

# WORDPRESS_NAMESPACE stores the XML namespace used by WordPress export fields.
WORDPRESS_NAMESPACE = "{http://wordpress.org/export/1.2/}"

# CONTENT_NAMESPACE stores the XML namespace used for full post and page HTML bodies.
CONTENT_NAMESPACE = "{http://purl.org/rss/1.0/modules/content/}"

# OUTPUT_FILES stores the generated root-level files served by GitHub Pages.
OUTPUT_FILES = {
    "index": ROOT_DIRECTORY / "index.html",
    "not_found": ROOT_DIRECTORY / "404.html",
    "sitemap": ROOT_DIRECTORY / "sitemap.xml",
    "robots": ROOT_DIRECTORY / "robots.txt",
}

# OUTPUT_MEDIA_DIRECTORY stores the copied local media files.
OUTPUT_MEDIA_DIRECTORY = ROOT_DIRECTORY / "media"

# PAGE_COMMENT_PATTERN removes Gutenberg comment wrappers while keeping the actual HTML blocks.
PAGE_COMMENT_PATTERN = re.compile(r"<!--\s*/?wp:[\s\S]*?-->")

# PDF_BLOCK_PATTERN matches the WordPress PDF embed comment block used on the home page.
PDF_BLOCK_PATTERN = re.compile(r"<!--\s*wp:pdfemb/pdf-embedder-viewer\s+(\{.*?\})\s*/-->")

# SHORTCODE_EMBED_PATTERN matches legacy embed shortcodes wrapped around remote media URLs.
SHORTCODE_EMBED_PATTERN = re.compile(r"\[embed[^\]]*](https?://.+?)\[/embed]", re.IGNORECASE)

# SLIDESHARE_WRAPPER_PATTERN matches the wrapper left behind by the WordPress SlideShare block.
SLIDESHARE_WRAPPER_PATTERN = re.compile(
    r"<figure class=\"wp-block-embed-slideshare[\s\S]*?<div class=\"wp-block-embed__wrapper\">\s*(https?://[^<\s]+)\s*</div></figure>",
    re.IGNORECASE,
)

# ABSOLUTE_URL_PATTERN finds absolute URLs that may need to be rewritten to local static paths.
ABSOLUTE_URL_PATTERN = re.compile(r"https?://[^\s\"'<>\)]+")

# DIMENSION_SUFFIX_PATTERN detects resized WordPress image suffixes like -300x225.
DIMENSION_SUFFIX_PATTERN = re.compile(r"-\d+x\d+$", re.IGNORECASE)

# FILENAME_PATTERN finds filenames inside attachment metadata blobs.
FILENAME_PATTERN = re.compile(r"[^\"';/\\]+?\.(?:jpg|jpeg|png|gif|pdf|doc|docx)", re.IGNORECASE)


@dataclass(frozen=True)
class PageData:
    """One published WordPress page that should become a static HTML page."""

    title: str
    slug: str
    order: int
    body_html: str


@dataclass(frozen=True)
class SiteData:
    """The site-wide metadata and pages extracted from the WordPress export."""

    title: str
    description: str
    pages: list[PageData]
    media_url_map: dict[str, str]


def find_primary_export_file() -> Path:
    """Find the main WordPress export XML file and ignore the media-only export."""

    # export_files stores all XML files inside the export folder.
    export_files = sorted(EXPORT_DIRECTORY.glob("*.xml"))
    # primary_files keeps only the main content export candidates.
    primary_files = [path for path in export_files if "media" not in path.name.lower()]
    if not primary_files:
        raise FileNotFoundError("Could not find the main WordPress export XML file.")
    return primary_files[-1]


def parse_menu_order(value: str | None) -> int:
    """Convert WordPress menu order text into a stable integer sort key."""

    return int(value or 0)


def build_media_lookup() -> dict[str, str]:
    """Build a case-insensitive lookup from media filenames to their real filenames."""

    # media_lookup stores lowercase names mapped to the exact filename on disk.
    media_lookup: dict[str, str] = {}
    for path in MEDIA_LIBRARY_DIRECTORY.iterdir():
        if path.is_file():
            media_lookup[path.name.lower()] = path.name
    return media_lookup


def resolve_media_filename(requested_name: str, media_lookup: dict[str, str]) -> str | None:
    """Resolve a referenced upload filename to the closest matching local media file."""

    # requested_path stores the parsed filename components.
    requested_path = Path(requested_name)
    # suffix stores the lowercase extension used by the local media file.
    suffix = requested_path.suffix.lower()
    # stem stores the filename without the extension.
    stem = requested_path.stem
    # base_stem removes WordPress thumbnail dimensions when present.
    base_stem = DIMENSION_SUFFIX_PATTERN.sub("", stem)
    # candidate_names stores the prioritized filename guesses.
    candidate_names = [
        requested_path.name,
        f"{base_stem}{suffix}",
        f"{base_stem}-scaled{suffix}",
    ]
    if stem.endswith("-scaled"):
        # unscaled_name checks for files where WordPress content references the scaled original.
        candidate_names.append(f"{stem[:-7]}{suffix}")
    else:
        # scaled_name checks for files where only the -scaled original was exported locally.
        candidate_names.append(f"{stem}-scaled{suffix}")

    # seen_names prevents duplicate candidate checks.
    seen_names: set[str] = set()
    for candidate_name in candidate_names:
        # normalized_name stores the lowercase lookup key.
        normalized_name = candidate_name.lower()
        if normalized_name in seen_names:
            continue
        seen_names.add(normalized_name)
        if normalized_name in media_lookup:
            return media_lookup[normalized_name]
    return None


def extract_attachment_urls(item: ET.Element) -> set[str]:
    """Collect the attachment URL and any size variants recorded in metadata."""

    # attachment_urls stores every public upload URL that may appear in page HTML.
    attachment_urls: set[str] = set()
    # attachment_url stores the canonical URL of the attachment item.
    attachment_url = item.findtext(f"{WORDPRESS_NAMESPACE}attachment_url") or ""
    if not attachment_url:
        return attachment_urls
    attachment_urls.add(attachment_url)

    # attachment_directory stores the public uploads directory for the attachment.
    attachment_directory = attachment_url.rsplit("/", 1)[0]
    for meta in item.findall(f"{WORDPRESS_NAMESPACE}postmeta"):
        # meta_key stores the name of the current attachment metadata field.
        meta_key = meta.findtext(f"{WORDPRESS_NAMESPACE}meta_key") or ""
        if meta_key != "_wp_attachment_metadata":
            continue
        # metadata_text stores the PHP-serialized attachment metadata blob.
        metadata_text = meta.findtext(f"{WORDPRESS_NAMESPACE}meta_value") or ""
        for filename in FILENAME_PATTERN.findall(metadata_text):
            attachment_urls.add(f"{attachment_directory}/{filename}")
    return attachment_urls


def build_media_url_map(channel: ET.Element) -> dict[str, str]:
    """Map WordPress upload URLs to the local GitHub Pages media directory."""

    # media_lookup stores the exported local files by filename.
    media_lookup = build_media_lookup()
    # media_url_map stores rewritten public upload URLs to local static paths.
    media_url_map: dict[str, str] = {}
    for item in channel.findall("item"):
        # post_type stores the kind of WordPress item currently being inspected.
        post_type = item.findtext(f"{WORDPRESS_NAMESPACE}post_type")
        if post_type != "attachment":
            continue
        for attachment_url in extract_attachment_urls(item):
            # requested_name stores the filename portion referenced by the page HTML.
            requested_name = Path(urlparse(attachment_url).path).name
            # resolved_name stores the best matching local exported filename.
            resolved_name = resolve_media_filename(requested_name, media_lookup)
            if resolved_name:
                media_url_map[attachment_url] = f"/media/{resolved_name}"
    return media_url_map


def load_site_data() -> SiteData:
    """Parse the WordPress XML export into site metadata, pages, and media mappings."""

    # export_path stores the main XML file selected from the export directory.
    export_path = find_primary_export_file()
    # root stores the parsed XML tree root.
    root = ET.parse(export_path).getroot()
    # channel stores the main RSS channel element containing pages and attachments.
    channel = root.find("channel")
    if channel is None:
        raise ValueError("The WordPress export is missing the channel element.")

    # pages stores the published WordPress pages that should become static pages.
    pages: list[PageData] = []
    for item in channel.findall("item"):
        # post_type stores the kind of WordPress item currently being inspected.
        post_type = item.findtext(f"{WORDPRESS_NAMESPACE}post_type")
        # status stores the publication status for the current item.
        status = item.findtext(f"{WORDPRESS_NAMESPACE}status")
        if post_type != "page" or status != "publish":
            continue
        # title stores the public page title.
        title = item.findtext("title") or ""
        # slug stores the page slug used for the output folder path.
        slug = item.findtext(f"{WORDPRESS_NAMESPACE}post_name") or ""
        # order stores the menu order used for site navigation.
        order = parse_menu_order(item.findtext(f"{WORDPRESS_NAMESPACE}menu_order"))
        # body_html stores the raw HTML fragment exported by WordPress.
        body_html = item.findtext(f"{CONTENT_NAMESPACE}encoded") or ""
        pages.append(PageData(title=title, slug=slug, order=order, body_html=body_html))

    # sorted_pages keeps the public pages in the same order as the original menu.
    sorted_pages = sorted(pages, key=lambda page: (page.order, page.title.lower()))
    # site_title stores the original WordPress site title.
    site_title = channel.findtext("title") or ""
    # site_description stores the original WordPress site tagline.
    site_description = channel.findtext("description") or ""
    # media_url_map stores rewritten upload URLs to local static media files.
    media_url_map = build_media_url_map(channel)
    return SiteData(title=site_title, description=site_description, pages=sorted_pages, media_url_map=media_url_map)


def rewrite_known_url(url: str, page_lookup: dict[str, PageData], media_url_map: dict[str, str]) -> str:
    """Rewrite WordPress internal and upload URLs to static GitHub Pages paths."""

    # normalized_url decodes HTML entities before URL parsing.
    normalized_url = html.unescape(url)
    if normalized_url in media_url_map:
        return media_url_map[normalized_url]

    # parsed_url stores the structured URL components.
    parsed_url = urlparse(normalized_url)
    # hostname stores the lowercase host for internal-link detection.
    hostname = (parsed_url.netloc or "").lower()
    if hostname not in {"shalyt.com", "www.shalyt.com", ""}:
        return url

    # path stores the URL path used to route to pages or uploads.
    path = parsed_url.path or "/"
    if path in {"", "/", "/home", "/home/"}:
        return "/"
    if path.startswith("/wp-content/uploads/"):
        # upload_url checks the full URL first.
        upload_url = normalized_url
        if upload_url in media_url_map:
            return media_url_map[upload_url]
        # fallback_url checks the path against the canonical shalyt.com host.
        fallback_url = f"http://shalyt.com{path}"
        if fallback_url in media_url_map:
            return media_url_map[fallback_url]
    # slug stores the first path segment used to identify internal pages.
    slug = path.strip("/").split("/", 1)[0]
    if slug in page_lookup:
        return "/" if slug == "home" else f"/{slug}/"
    return url


def build_pdf_embed_html(url: str, page_lookup: dict[str, PageData], media_url_map: dict[str, str]) -> str:
    """Convert the WordPress PDF block into a static inline PDF viewer."""

    # rewritten_url stores the local static path or the original URL fallback.
    rewritten_url = rewrite_known_url(url, page_lookup, media_url_map)
    # escaped_url stores the PDF path safely escaped for HTML attributes.
    escaped_url = html.escape(rewritten_url, quote=True)
    return (
        '<div class="pdf-embed">'
        f'<object data="{escaped_url}" type="application/pdf">'
        f'<p><a href="{escaped_url}">Open the PDF document</a></p>'
        "</object>"
        "</div>"
    )


def replace_pdf_blocks(content_html: str, page_lookup: dict[str, PageData], media_url_map: dict[str, str]) -> str:
    """Replace WordPress PDF block comments with a static PDF object viewer."""

    def replacement(match: re.Match[str]) -> str:
        """Build the replacement HTML for one PDF block match."""

        # block_json stores the serialized JSON object embedded in the comment.
        block_json = match.group(1)
        # block_data stores the parsed block configuration.
        block_data = json.loads(block_json)
        # pdf_url stores the original PDF URL referenced by the block.
        pdf_url = block_data.get("url", "")
        return build_pdf_embed_html(pdf_url, page_lookup, media_url_map)

    return PDF_BLOCK_PATTERN.sub(replacement, content_html)


def build_youtube_embed_html(url: str) -> str:
    """Convert a YouTube watch URL into a responsive iframe embed."""

    # parsed_url stores the structured URL components for the incoming video link.
    parsed_url = urlparse(html.unescape(url))
    # query_parameters stores the decoded query string parameters.
    query_parameters = parse_qs(parsed_url.query)
    # video_id stores the YouTube video identifier.
    video_id = query_parameters.get("v", [""])[0]
    # playlist_id stores the optional playlist identifier.
    playlist_id = query_parameters.get("list", [""])[0]
    if not video_id:
        # escaped_url stores the fallback URL when an iframe cannot be created.
        escaped_url = html.escape(url, quote=True)
        return f'<p class="external-embed"><a href="{escaped_url}">{escaped_url}</a></p>'

    # iframe_source stores the privacy-enhanced YouTube embed URL.
    iframe_source = f"https://www.youtube-nocookie.com/embed/{video_id}"
    if playlist_id:
        iframe_source += f"?list={playlist_id}"
    # escaped_source stores the iframe source safely escaped for HTML attributes.
    escaped_source = html.escape(iframe_source, quote=True)
    return (
        '<div class="video-embed">'
        f'<iframe src="{escaped_source}" title="YouTube video" loading="lazy" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
        'allowfullscreen></iframe>'
        "</div>"
    )


def replace_shortcode_embeds(content_html: str) -> str:
    """Replace legacy WordPress embed shortcodes with static embed HTML."""

    def replacement(match: re.Match[str]) -> str:
        """Build the replacement HTML for one embed shortcode match."""

        # embed_url stores the URL wrapped by the WordPress shortcode.
        embed_url = match.group(1).strip()
        return build_youtube_embed_html(embed_url)

    return SHORTCODE_EMBED_PATTERN.sub(replacement, content_html)


def replace_slideshare_wrappers(content_html: str) -> str:
    """Convert the SlideShare block wrapper into a normal external link block."""

    def replacement(match: re.Match[str]) -> str:
        """Build the replacement HTML for one SlideShare block match."""

        # slideshare_url stores the public SlideShare URL left in the wrapper.
        slideshare_url = match.group(1).strip()
        # escaped_url stores the link safely escaped for HTML output.
        escaped_url = html.escape(slideshare_url, quote=True)
        return f'<p class="external-embed"><a href="{escaped_url}">{escaped_url}</a></p>'

    return SLIDESHARE_WRAPPER_PATTERN.sub(replacement, content_html)


def strip_wordpress_comments(content_html: str) -> str:
    """Remove Gutenberg comment markers and keep the actual HTML blocks."""

    return PAGE_COMMENT_PATTERN.sub("", content_html)


def rewrite_absolute_urls(content_html: str, page_lookup: dict[str, PageData], media_url_map: dict[str, str]) -> str:
    """Rewrite absolute shalyt.com URLs in the page HTML to static local paths."""

    def replacement(match: re.Match[str]) -> str:
        """Build the replacement URL for one absolute URL match."""

        # original_url stores the matched URL from the page HTML.
        original_url = match.group(0)
        return rewrite_known_url(original_url, page_lookup, media_url_map)

    return ABSOLUTE_URL_PATTERN.sub(replacement, content_html)


def normalize_whitespace(content_html: str) -> str:
    """Tidy the exported HTML so the generated files stay readable and stable."""

    # normalized_html collapses repeated blank lines left behind by comment stripping.
    normalized_html = re.sub(r"\n{3,}", "\n\n", content_html)
    return normalized_html.strip() + "\n"


def rewrite_content_html(content_html: str, page_lookup: dict[str, PageData], media_url_map: dict[str, str]) -> str:
    """Rewrite one exported page body into static-hosting-friendly HTML."""

    # rewritten_html stores the progressively transformed page HTML.
    rewritten_html = content_html
    rewritten_html = replace_pdf_blocks(rewritten_html, page_lookup, media_url_map)
    rewritten_html = replace_shortcode_embeds(rewritten_html)
    rewritten_html = replace_slideshare_wrappers(rewritten_html)
    rewritten_html = strip_wordpress_comments(rewritten_html)
    rewritten_html = rewrite_absolute_urls(rewritten_html, page_lookup, media_url_map)
    rewritten_html = normalize_whitespace(rewritten_html)
    return rewritten_html


def render_navigation(pages: list[PageData], active_slug: str) -> str:
    """Render the top navigation in the original page order."""

    # nav_links stores the rendered anchor elements for each published page.
    nav_links = []
    for page in pages:
        # target_href stores the local static path for the page.
        target_href = "/" if page.slug == "home" else f"/{page.slug}/"
        # active_class marks the current page inside the navigation.
        active_class = " class=\"is-active\"" if page.slug == active_slug else ""
        nav_links.append(
            f'<a href="{html.escape(target_href, quote=True)}"{active_class}>{html.escape(page.title)}</a>'
        )
    return '<nav class="site-nav">' + "".join(nav_links) + "</nav>"


def build_document(site_data: SiteData, page: PageData, page_html: str) -> str:
    """Wrap one page body in the shared site layout and metadata."""

    # is_home_page tracks whether the current page is the root landing page.
    is_home_page = page.slug == "home"
    # body_class stores a page-specific CSS hook for layout refinements.
    body_class = f"page-{page.slug}"
    # page_title stores the browser title for the current page.
    page_title = site_data.title if is_home_page else f"{page.title} | {site_data.title}"
    # canonical_url stores the canonical public URL for the current page.
    canonical_url = "https://shalyt.com/" if is_home_page else f"https://shalyt.com/{page.slug}/"
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8" />\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1" />\n'
        f"  <title>{html.escape(page_title)}</title>\n"
        f'  <meta name="description" content="{html.escape(site_data.description, quote=True)}" />\n'
        f'  <link rel="canonical" href="{html.escape(canonical_url, quote=True)}" />\n'
        '  <meta property="og:type" content="website" />\n'
        f'  <meta property="og:title" content="{html.escape(page_title, quote=True)}" />\n'
        f'  <meta property="og:description" content="{html.escape(site_data.description, quote=True)}" />\n'
        f'  <meta property="og:url" content="{html.escape(canonical_url, quote=True)}" />\n'
        '  <meta property="og:image" content="https://shalyt.com/media/cropped-IMG_7337_Grey.jpg" />\n'
        '  <link rel="icon" href="/media/cropped-IMG_7337_Grey.jpg" />\n'
        '  <link rel="stylesheet" href="/assets/styles.css" />\n'
        "</head>\n"
        f'<body class="{html.escape(body_class, quote=True)}">\n'
        '  <a class="skip-link" href="#content">Skip to content</a>\n'
        '  <header class="site-header">\n'
        '    <div class="site-brand">\n'
        f'      <a href="/">{html.escape(site_data.title)}</a>\n'
        f'      <p>{html.escape(site_data.description)}</p>\n'
        "    </div>\n"
        f"    {render_navigation(site_data.pages, page.slug)}\n"
        "  </header>\n"
        '  <main id="content" class="page-shell">\n'
        '    <article class="page-content">\n'
        f"{page_html}"
        "    </article>\n"
        "  </main>\n"
        '  <footer class="site-footer">\n'
        '    <p>Static rebuild generated from the local WordPress export for GitHub Pages.</p>\n'
        "  </footer>\n"
        "</body>\n"
        "</html>\n"
    )


def build_not_found_page(site_data: SiteData) -> str:
    """Build a simple 404 page with the same shared navigation layout."""

    # fallback_page stores a lightweight placeholder page used for shared layout rendering.
    fallback_page = PageData(title="Not Found", slug="404", order=999, body_html="")
    # page_html stores the visible body markup shown for unknown routes.
    page_html = (
        '<h1>Page not found</h1>\n'
        '<p>This page does not exist in the exported static version of shalyt.com.</p>\n'
        '<p><a href="/">Return to the home page</a>.</p>\n'
    )
    return build_document(site_data, fallback_page, page_html)


def page_output_path(slug: str) -> Path:
    """Return the primary output path for a page slug."""

    return OUTPUT_FILES["index"] if slug == "home" else ROOT_DIRECTORY / slug / "index.html"


def page_alias_path(slug: str) -> Path | None:
    """Return an optional alias path used to preserve the old home slug."""

    return ROOT_DIRECTORY / "home" / "index.html" if slug == "home" else None


def write_text_file(path: Path, content: str) -> None:
    """Write a UTF-8 text file and create its parent folder when needed."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_media_library() -> None:
    """Copy the exported media library into the GitHub Pages media folder."""

    OUTPUT_MEDIA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    for source_path in MEDIA_LIBRARY_DIRECTORY.iterdir():
        if not source_path.is_file():
            continue
        # destination_path stores the target file inside the static media folder.
        destination_path = OUTPUT_MEDIA_DIRECTORY / source_path.name
        shutil.copy2(source_path, destination_path)


def build_sitemap(site_data: SiteData) -> str:
    """Build a sitemap covering the generated static pages."""

    # page_urls stores the canonical URLs for the generated static pages.
    page_urls = ["https://shalyt.com/"]
    for page in site_data.pages:
        if page.slug == "home":
            page_urls.append("https://shalyt.com/home/")
        else:
            page_urls.append(f"https://shalyt.com/{page.slug}/")
    page_urls.append("https://shalyt.com/404.html")
    # url_entries stores the XML entries for each sitemap URL.
    url_entries = [f"<url><loc>{html.escape(url)}</loc></url>" for url in page_urls]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(url_entries)
        + "\n</urlset>\n"
    )


def build_robots_txt() -> str:
    """Build a simple robots.txt file that points crawlers to the sitemap."""

    return "User-agent: *\nAllow: /\nSitemap: https://shalyt.com/sitemap.xml\n"


def build_ramanujan_poster_html() -> str:
    """Render the optional Ramanujan poster photo when a local asset is available."""

    # candidate_names stores the accepted filenames for a manually added poster photo.
    candidate_names = [
        "ramanujan-machine-neurips-2024.jpg",
        "ramanujan-machine-neurips-2024.png",
        "neurips-2024-poster.jpg",
        "neurips-2024-poster.png",
    ]
    for candidate_name in candidate_names:
        # candidate_path stores the expected copied media path for the poster image.
        candidate_path = OUTPUT_MEDIA_DIRECTORY / candidate_name
        if candidate_path.exists():
            return (
                '<figure class="wp-block-image">'
                f'<img src="/media/{html.escape(candidate_name, quote=True)}" alt="Presenting the NeurIPS 2024 poster." />'
                '<figcaption>Presenting the NeurIPS 2024 poster.</figcaption>'
                '</figure>\n'
            )
    return ""


def build_ramanujan_machine_section() -> str:
    """Build the requested AI section that sits above the exported Evo.Do content."""

    # poster_html stores the optional poster markup when the local asset is present.
    poster_html = build_ramanujan_poster_html()
    return (
        '<h2><strong><span style="text-decoration: underline;">Ramanujan Machine</span></strong></h2>\n\n'
        '<p>I currently lead the Ramanujan Machine group under Professor Ido Kaminer, working on the intersection of AI and experimental mathematics. The field is changing very quickly: models, symbolic tools and automated search pipelines now let us explore mathematical spaces that were previously too large to investigate by hand.</p>\n\n'
        '<p>Our recent work includes the <a href="https://www.ramanujanmachine.com/asymob-algebraic-symbolic-mathematical-operations-benchmark/">ASyMOB</a> benchmark for algebraic symbolic reasoning, the <a href="https://www.ramanujanmachine.com/results/from-euler-to-ai-unifying-formulas-for-mathematical-constants/">From Euler to AI</a> line on unifying formulas for mathematical constants, and the broader <a href="https://www.ramanujanmachine.com/">Ramanujan Machine</a> effort to turn mathematical discovery into a scalable experimental process. Published outputs from this work include <a href="https://arxiv.org/abs/2505.23851">ASyMOB</a>, <a href="https://arxiv.org/abs/2507.08138">From Euler to AI</a>, the <a href="https://neurips.cc/virtual/2025/loc/san-diego/poster/117099">NeurIPS 2025 poster</a>, the <a href="https://neurips.cc/virtual/2024/poster/95491">NeurIPS 2024 poster</a>, and our <a href="https://www.pnas.org/doi/10.1073/pnas.2321440121">PNAS paper</a>.</p>\n\n'
        '<p>One example of that direction is the work around conservative matrix fields and automated conjecture generation: combining AI with careful mathematical experimentation to surface structure, cluster families of formulas and suggest new paths for human insight. This short talk gives a quick taste of that line of work:</p>\n\n'
        '<div style="text-align:center;">\n'
        '<div class="video-embed"><iframe src="https://www.youtube-nocookie.com/embed/Uk04gfIt8yM" title="Conservative matrix fields talk" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>\n'
        '</div>\n\n'
        f'{poster_html}'
    )


def build_pages(site_data: SiteData) -> None:
    """Rewrite every page and write it to the correct static output path."""

    # page_lookup stores the pages by slug for fast internal-link rewriting.
    page_lookup = {page.slug: page for page in site_data.pages}
    for page in site_data.pages:
        # rewritten_html stores the transformed body HTML for the current page.
        rewritten_html = rewrite_content_html(page.body_html, page_lookup, site_data.media_url_map)
        if page.slug == "ai":
            # manual_intro_html stores the explicitly requested AI section added above Evo.Do.
            manual_intro_html = build_ramanujan_machine_section()
            rewritten_html = manual_intro_html + rewritten_html
        # document_html stores the final wrapped HTML document.
        document_html = build_document(site_data, page, rewritten_html)
        write_text_file(page_output_path(page.slug), document_html)
        # alias_path stores the optional extra output path for the current page.
        alias_path = page_alias_path(page.slug)
        if alias_path is not None:
            write_text_file(alias_path, document_html)


def main() -> None:
    """Generate the full static site from the local WordPress export and media files."""

    # site_data stores the parsed export metadata, pages, and media URL mappings.
    site_data = load_site_data()
    copy_media_library()
    build_pages(site_data)
    write_text_file(OUTPUT_FILES["not_found"], build_not_found_page(site_data))
    write_text_file(OUTPUT_FILES["sitemap"], build_sitemap(site_data))
    write_text_file(OUTPUT_FILES["robots"], build_robots_txt())


if __name__ == "__main__":
    main()



