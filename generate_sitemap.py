import os
from datetime import datetime

BASE_URL = "https://rhoclouds.github.io"
BLOG_DIR = "blog"
STATIC_PAGES = ["index.html", "blog.html", "library.html"]

def find_blog_html_files():
    html_files = []
    for root, _, files in os.walk(BLOG_DIR):
        for file in files:
            if file.endswith(".html") and "template" not in file.lower():
                full_path = os.path.join(root, file).replace("\\", "/")
                html_files.append(full_path)
    return html_files

def generate_sitemap(blog_files):
    header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    header += '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">\n'
    body = ""
    today = datetime.now().strftime("%Y-%m-%d")

    # Static top-level pages
    for static_page in STATIC_PAGES:
        url = f"{BASE_URL}/{static_page}"
        body += f"  <url>\n"
        body += f"    <loc>{url}</loc>\n"
        body += f"    <lastmod>{today}</lastmod>\n"
        body += f"    <changefreq>monthly</changefreq>\n"
        body += f"    <priority>1.0</priority>\n"
        body += f"  </url>\n"

    # Blog
    for file in sorted(blog_files):
        url = f"{BASE_URL}/{file}"
        body += f"  <url>\n"
        body += f"    <loc>{url}</loc>\n"
        body += f"    <lastmod>{today}</lastmod>\n"
        body += f"    <changefreq>monthly</changefreq>\n"
        body += f"    <priority>0.8</priority>\n"
        body += f"  </url>\n"

    footer = "</urlset>"
    return header + body + footer

if __name__ == "__main__":
    blog_files = find_blog_html_files()
    sitemap = generate_sitemap(blog_files)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap)
    print(f"Generated sitemap.xml with {len(blog_files)} blog posts + {len(STATIC_PAGES)} static pages.")