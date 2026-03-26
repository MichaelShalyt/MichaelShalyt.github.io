"""Unit tests for the WordPress-export-driven static site generator."""

from pathlib import Path
import unittest

from scripts import build_site


class BuildSiteTests(unittest.TestCase):
    """Validate the main parsing and generation flows."""

    def test_load_site_data_keeps_original_page_order(self) -> None:
        """Published pages should preserve the original WordPress menu order."""

        # site_data stores the parsed metadata and page list from the export.
        site_data = build_site.load_site_data()
        self.assertEqual([page.slug for page in site_data.pages], ["home", "ai", "cyber-security", "physics", "games", "ideas-2"])

    def test_media_filename_resolution_handles_thumbnail_variants(self) -> None:
        """Thumbnail references should resolve to the exported original media files."""

        # media_lookup stores the exported local media files by lowercase filename.
        media_lookup = build_site.build_media_lookup()
        resolved_name = build_site.resolve_media_filename("20171225_172602-300x225.jpg", media_lookup)
        self.assertEqual(resolved_name, "20171225_172602-scaled.jpg")

    def test_rewrite_content_html_converts_uploads_internal_links_and_embeds(self) -> None:
        """Page rewriting should preserve content while making it static-hosting-friendly."""

        # site_data stores the parsed metadata and page list from the export.
        site_data = build_site.load_site_data()
        # page_lookup stores the site pages by slug for URL rewriting.
        page_lookup = {page.slug: page for page in site_data.pages}
        sample_html = (
            '<p><a href="http://shalyt.com/ai/">AI</a></p>'
            '<p><a href="http://shalyt.com/wp-content/uploads/2025/02/MichaelShalyt_2025_anon.pdf">CV</a></p>'
            '[embed width="560" height="420"]https://www.youtube.com/watch?v=liHOaiCklQw[/embed]'
            '<!-- wp:pdfemb/pdf-embedder-viewer {"pdfID":173,"url":"http://shalyt.com/wp-content/uploads/2025/02/MichaelShalyt_2025_anon.pdf"} /-->'
        )
        rewritten_html = build_site.rewrite_content_html(sample_html, page_lookup, site_data.media_url_map)
        self.assertIn('href="/ai/"', rewritten_html)
        self.assertIn('href="/media/MichaelShalyt_2025_anon.pdf"', rewritten_html)
        self.assertIn('youtube-nocookie.com/embed/liHOaiCklQw', rewritten_html)
        self.assertIn('data="/media/MichaelShalyt_2025_anon.pdf"', rewritten_html)

    def test_build_outputs_expected_pages_and_media(self) -> None:
        """The generator should write the static pages and copy the media files."""

        build_site.main()
        self.assertTrue(Path(build_site.OUTPUT_FILES["index"]).exists())
        ai_path = build_site.ROOT_DIRECTORY / "ai" / "index.html"
        self.assertTrue(ai_path.exists())
        self.assertTrue((build_site.ROOT_DIRECTORY / "home" / "index.html").exists())
        self.assertTrue((build_site.OUTPUT_MEDIA_DIRECTORY / "MichaelShalyt_2025_anon.pdf").exists())
        ai_html = ai_path.read_text(encoding="utf-8")
        self.assertIn("Ramanujan Machine", ai_html)
        self.assertIn("Uk04gfIt8yM", ai_html)


if __name__ == "__main__":
    unittest.main()

