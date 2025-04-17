import os
from datetime import datetime

BASE_URL = "https://rhoclouds.github.io"
BLOG_DIR = "blog"

def find_blog_html_files():
    html_files = []
    for root, _, files in os.walk(BLOG_DIR):
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file).replace("\\", "/")
                html_files.append(full_path)
    return html_files

def generate_sitemap(files):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    header += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body = ""
    for file in sorted(files):
        url = f"{BASE_URL}/{file}"
        lastmod = datetime.now().strftime("%Y-%m-%d")
        body += f"  <url>\n"
        body += f"    <loc>{url}</loc>\n"
        body += f"    <lastmod>{lastmod}</lastmod>\n"
        body += f"    <changefreq>monthly</changefreq>\n"
        body += f"    <priority>0.8</priority>\n"
        body += f"  </url>\n"
    footer = "</urlset>"
    return header + body + footer

if __name__ == "__main__":
    html_files = find_blog_html_files()
    sitemap = generate_sitemap(html_files)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Generated sitemap.xml with {len(html_files)} blog posts.")