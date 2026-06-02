# Michael Shalyt

Personal website for Michael Shalyt, covering AI, cybersecurity, physics, games, and ideas.

This repository contains the static website published at `shalyt.com` and `michaelshalyt.github.io`.

## Main Usage Flows

### Rebuild The Static Site

Use this after changing content in `content/site_content.py`.

```powershell
python scripts\build_site.py
python -m unittest discover -s tests -v
```

### Update The CV

Put the current CV PDF in `media/`, update the CV iframe path in `content/site_content.py`, rebuild the generated HTML, and run the tests.

Example:

```powershell
python scripts\build_site.py
python -m unittest discover -s tests -v
```

The current published CV path is `/media/MichaelShalyt_2026.pdf`.

### Publish To GitHub Pages

Commit the source updates, generated HTML, and media changes, then push to the GitHub Pages branch.

Example:

```powershell
git add content\site_content.py tests\test_build_site.py README.md index.html home\index.html media\MichaelShalyt_2026.pdf
git commit -m "Update CV PDF"
git push
```
