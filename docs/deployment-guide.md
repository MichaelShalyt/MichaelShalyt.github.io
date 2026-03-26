# Deployment Guide

## Goal

Publish the generated static site as `shalyt.com` on GitHub Pages.

## Local steps before publishing

1. Run `python scripts/build_site.py`.
2. Run `python -m unittest discover -s tests -v`.
3. Confirm the generated pages exist:
   - [index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/index.html)
   - [ai/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/ai/index.html)
   - [cyber-security/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/cyber-security/index.html)
   - [physics/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/physics/index.html)
   - [games/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/games/index.html)
   - [ideas-2/index.html](D:/Codex%20Projects/Shalyt%20Website%20Migration/ideas-2/index.html)
4. Commit and push the repository to GitHub.

## GitHub Pages setup

1. Create a GitHub repository for the site.
2. Push this workspace into that repository.
3. In GitHub, open `Settings -> Pages`.
4. Set `Deploy from a branch`.
5. Choose the main branch and the root folder.
6. Save.

## Domain setup for `shalyt.com`

Keep [CNAME](D:/Codex%20Projects/Shalyt%20Website%20Migration/CNAME) in the repository root with `shalyt.com`.

At the DNS provider:

1. Add A records for `shalyt.com`:
   - `185.199.108.153`
   - `185.199.109.153`
   - `185.199.110.153`
   - `185.199.111.153`
2. Add a CNAME record for `www` pointing to your GitHub Pages hostname.
3. After the site resolves in GitHub Pages settings, enable HTTPS.

## Example update cycle

```powershell
python scripts/build_site.py
python -m unittest discover -s tests -v
git add .
git commit -m "Update website content"
git push
```

