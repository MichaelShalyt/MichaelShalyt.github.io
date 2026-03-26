# Design and Compatibility Notes

## What stayed the same

1. The page inventory comes directly from the WordPress export.
2. The page body content is taken from the exported HTML, not rewritten by hand.
3. The media files come from the provided media library.

## What changed only for GitHub Pages compatibility

1. WordPress editor comments were removed because they are not rendered page content.
2. Internal `shalyt.com` links were rewritten to static folder routes such as `/ai/` and `/physics/`.
3. `wp-content/uploads` URLs were rewritten to the generated local `/media/` folder.
4. WordPress shortcode embeds were converted to static iframe or link equivalents.
5. The home-page PDF block was converted to an inline PDF object so it works without WordPress plugins.

## What was intentionally not done

1. No extra profile sections were added.
2. No outside biography or publication data was merged in.
3. No content was rewritten into a new information architecture.
