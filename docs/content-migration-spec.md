# Migration Notes

This migration now uses only the local WordPress export and the provided media library. It does not add inferred content from outside profiles or external public sources.

## Source of truth

- [Original Website Content/michaelshalyt.WordPress.2026-03-26.xml](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content/michaelshalyt.WordPress.2026-03-26.xml)
- [Original Website Content/Media Library](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content/Media%20Library)

## Published pages detected in the export

1. Home
2. AI
3. Cyber Security
4. Physics
5. Games
6. Ideas

## Static-hosting transformations

1. The page text, headings, links, and exported HTML are preserved.
2. WordPress block comments are removed because they are editor metadata, not page content.
3. `shalyt.com` internal links are rewritten to local static routes.
4. Upload URLs are rewritten to the copied local [media](D:/Codex%20Projects/Shalyt%20Website%20Migration/media) folder.
5. WordPress embed shortcodes are replaced with static equivalents that GitHub Pages can serve.
