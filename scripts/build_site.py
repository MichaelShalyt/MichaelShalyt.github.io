"""Build the static website from curated local source content."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
import sys

# ROOT_DIRECTORY stores the repository root used for generated output.
ROOT_DIRECTORY = Path(__file__).resolve().parents[1]

# sys.path is extended so the build script can be run directly from the repository root.
sys.path.insert(0, str(ROOT_DIRECTORY))

from content.site_content import PAGE_DATA
from content.site_content import SITE_DESCRIPTION
from content.site_content import SITE_TITLE

# OUTPUT_FILES stores the generated root-level files served by GitHub Pages.
OUTPUT_FILES = {
    "index": ROOT_DIRECTORY / "index.html",
    "not_found": ROOT_DIRECTORY / "404.html",
    "sitemap": ROOT_DIRECTORY / "sitemap.xml",
    "robots": ROOT_DIRECTORY / "robots.txt",
}


@dataclass(frozen=True)
class PageData:
    """One published website page rendered as a standalone static HTML file."""

    title: str
    slug: str
    order: int
    body_html: str


@dataclass(frozen=True)
class SiteData:
    """The shared site metadata and ordered page list."""

    title: str
    description: str
    pages: list[PageData]


def load_site_data() -> SiteData:
    """Load the curated static page source from the repository content module."""

    # pages stores the ordered page definitions loaded from the content module.
    pages = [PageData(**page) for page in PAGE_DATA]
    return SiteData(title=SITE_TITLE, description=SITE_DESCRIPTION, pages=pages)


def render_navigation(pages: list[PageData], active_slug: str) -> str:
    """Render the top navigation in the configured page order."""

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

        "</body>\n"
        "</html>\n"
    )


def build_not_found_page(site_data: SiteData) -> str:
    """Build a simple 404 page with the shared navigation layout."""

    # fallback_page stores a lightweight placeholder page used for shared layout rendering.
    fallback_page = PageData(title="Not Found", slug="404", order=999, body_html="")
    # page_html stores the visible body markup shown for unknown routes.
    page_html = (
        '<h1>Page not found</h1>\n'
        '<p>This page does not exist on shalyt.com.</p>\n'
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


def build_pages(site_data: SiteData) -> None:
    """Write every configured page to the correct static output path."""

    for page in site_data.pages:
        # document_html stores the final wrapped HTML document.
        document_html = build_document(site_data, page, page.body_html)
        write_text_file(page_output_path(page.slug), document_html)
        # alias_path stores the optional extra output path for the current page.
        alias_path = page_alias_path(page.slug)
        if alias_path is not None:
            write_text_file(alias_path, document_html)


def main() -> None:
    """Generate the full static site from the curated local source content."""

    # site_data stores the shared metadata and ordered page list.
    site_data = load_site_data()
    build_pages(site_data)
    write_text_file(OUTPUT_FILES["not_found"], build_not_found_page(site_data))
    write_text_file(OUTPUT_FILES["sitemap"], build_sitemap(site_data))
    write_text_file(OUTPUT_FILES["robots"], build_robots_txt())


if __name__ == "__main__":
    main()

