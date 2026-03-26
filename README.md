# Shalyt Website Migration

This repository rebuilds `shalyt.com` as a static GitHub Pages site directly from the local WordPress export in [Original Website Content](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content). The generator does not infer or add outside profile content. It takes the exported page HTML and media library as the only source of truth, then rewrites just the WordPress-specific pieces that do not work on GitHub Pages.

## Repository structure

- [Original Website Content](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content): the WordPress XML export and the provided media library.
- [scripts/build_site.py](D:/Codex%20Projects/Shalyt%20Website%20Migration/scripts/build_site.py): the generator that parses the export and writes the static site.
- [assets/styles.css](D:/Codex%20Projects/Shalyt%20Website%20Migration/assets/styles.css): the shared styling for the generated pages.
- [tests/test_build_site.py](D:/Codex%20Projects/Shalyt%20Website%20Migration/tests/test_build_site.py): unit tests for parsing, rewriting, and output generation.
- [media](D:/Codex%20Projects/Shalyt%20Website%20Migration/media): generated copy of the exported media library.

## Main usage flows

### 1. Rebuild the site from the export

Run:

```powershell
python scripts/build_site.py
```

This reads the WordPress export, copies the local media library, and regenerates:

- [index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/index.html)
- [home/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/home/index.html)
- [ai/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/ai/index.html)
- [cyber-security/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/cyber-security/index.html)
- [physics/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/physics/index.html)
- [games/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/games/index.html)
- [ideas-2/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/ideas-2/index.html)
- [media](D:/Codex%20Projects/Shalyt%20Website%20Migration/media)

### 2. Validate the main functionality

Run:

```powershell
python -m unittest discover -s tests -v
```

The tests validate the export parsing, media URL rewriting, embed conversion, and expected output files.

### 3. Replace the source export later

If you export the WordPress site again:

1. Replace the XML file in [Original Website Content](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content).
2. Replace the files in [Original Website Content/Media Library](D:/Codex%20Projects/Shalyt%20Website%20Migration/Original%20Website%20Content/Media%20Library) with the new media export.
3. Run `python scripts/build_site.py`.
4. Run `python -m unittest discover -s tests -v`.

### 4. Publish to GitHub Pages

Follow [docs/deployment-guide.md](D:/Codex%20Projects/Shalyt%20Website%20Migration/docs/deployment-guide.md).

## What the generator changes

The site content itself stays as exported. The generator only makes the minimum technical changes required for static hosting:

- strips WordPress block comments
- rewrites `shalyt.com` internal links to local static paths
- rewrites `wp-content/uploads` URLs to the copied [media](D:/Codex%20Projects/Shalyt%20Website%20Migration/media) folder
- converts YouTube shortcodes into iframe embeds
- converts the PDF embed block into a static inline PDF viewer

