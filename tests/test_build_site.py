"""Unit tests for the curated static site generator."""

from pathlib import Path
import unittest

from scripts import build_site


class BuildSiteTests(unittest.TestCase):
    """Validate the main page-loading and generation flows."""

    def test_load_site_data_keeps_expected_page_order(self) -> None:
        """Published pages should preserve the configured navigation order."""

        # site_data stores the shared metadata and page list loaded from content.
        site_data = build_site.load_site_data()
        self.assertEqual([page.slug for page in site_data.pages], ["home", "ai", "cyber-security", "physics", "games", "ideas-2"])

    def test_ai_page_source_contains_ramanujan_section(self) -> None:
        """The curated AI source should include the Ramanujan Machine addition."""

        # site_data stores the shared metadata and page list loaded from content.
        site_data = build_site.load_site_data()
        ai_page = next(page for page in site_data.pages if page.slug == "ai")
        self.assertIn("Ramanujan Machine", ai_page.body_html)
        self.assertIn("Uk04gfIt8yM", ai_page.body_html)
        self.assertIn("neurips-2024-poster.jpg", ai_page.body_html)

    def test_home_page_embeds_current_cv(self) -> None:
        """The home page should embed the current CV PDF from published media."""

        # site_data stores the shared metadata and page list loaded from content.
        site_data = build_site.load_site_data()
        # home_page stores the source HTML for the root landing page.
        home_page = next(page for page in site_data.pages if page.slug == "home")
        # current_cv_path stores the published PDF path served by GitHub Pages.
        current_cv_path = build_site.ROOT_DIRECTORY / "media" / "MichaelShalyt_2026.pdf"
        self.assertIn("/media/MichaelShalyt_2026.pdf", home_page.body_html)
        self.assertNotIn("/media/MichaelShalyt_2025_anon.pdf", home_page.body_html)
        self.assertTrue(current_cv_path.exists())

    def test_build_document_sets_page_specific_body_class(self) -> None:
        """Rendered pages should expose a page-specific body class for styling hooks."""

        page = build_site.PageData(title="Games", slug="games", order=5, body_html="<p>Body</p>\n")
        site_data = build_site.SiteData(title="Michael Shalyt", description="Yesterday You Said Tomorrow.", pages=[page])
        document = build_site.build_document(site_data, page, page.body_html)
        self.assertIn('<body class="page-games">', document)
        self.assertIn("Yesterday You Said Tomorrow.", document)

    def test_build_outputs_expected_pages(self) -> None:
        """The generator should write the expected static pages and route aliases."""

        build_site.main()
        self.assertTrue(Path(build_site.OUTPUT_FILES["index"]).exists())
        self.assertTrue((build_site.ROOT_DIRECTORY / "ai" / "index.html").exists())
        self.assertTrue((build_site.ROOT_DIRECTORY / "home" / "index.html").exists())
        ai_html = (build_site.ROOT_DIRECTORY / "ai" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Ramanujan Machine", ai_html)
        self.assertIn("Uk04gfIt8yM", ai_html)


if __name__ == "__main__":
    unittest.main()
