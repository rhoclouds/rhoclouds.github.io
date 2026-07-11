#!/usr/bin/env python3
# made by rhoclouds
"""Optimize static HTML exported from MATLAB Live Scripts.

Safe defaults:
  * Extract base64-embedded images into an assets directory.
  * Deduplicate identical embedded images by SHA-256 hash.
  * Move inline <style> blocks into one external CSS file.
  * Remove exact duplicate top-level CSS rules when tinycss2 is available.
  * Preserve document markup and MATLAB output structures.

The original file is never modified.
"""

# usage: "python matlab_optimizer.py projects/livescript.html --overwrite" if previous relics are still there


from __future__ import annotations

import argparse
import base64
import hashlib
import html as html_lib
import mimetypes
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import tinycss2  # type: ignore
except ImportError:
    tinycss2 = None

STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.IGNORECASE | re.DOTALL)
HEAD_CLOSE_RE = re.compile(r"</head\s*>", re.IGNORECASE)
HTML_DATA_IMAGE_RE = re.compile(
    r"(?P<prefix>\bsrc\s*=\s*)(?P<quote>['\"])(?P<data>data:image/[a-zA-Z0-9.+-]+(?:;[^,'\"]*)?,[^'\"]+)(?P=quote)",
    re.IGNORECASE,
)
CSS_DATA_IMAGE_RE = re.compile(
    r"url\(\s*(?P<quote>['\"]?)(?P<data>data:image/[a-zA-Z0-9.+-]+(?:;[^)'\"]*)?,[^)'\"]+)(?P=quote)\s*\)",
    re.IGNORECASE,
)

MIME_EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/gif": ".gif",
    "image/svg+xml": ".svg",
    "image/webp": ".webp",
    "image/bmp": ".bmp",
    "image/x-icon": ".ico",
    "image/vnd.microsoft.icon": ".ico",
}


@dataclass
class Stats:
    html_images_seen: int = 0
    css_images_seen: int = 0
    unique_images_written: int = 0
    duplicate_images_reused: int = 0
    style_blocks_externalized: int = 0
    duplicate_css_rules_removed: int = 0


def decode_data_uri(uri: str) -> Tuple[str, bytes]:
    header, payload = uri.split(",", 1)
    mediatype = header[5:].split(";", 1)[0].lower() or "application/octet-stream"
    is_base64 = ";base64" in header.lower()
    if is_base64:
        cleaned = re.sub(r"\s+", "", payload)
        data = base64.b64decode(cleaned, validate=False)
    else:
        from urllib.parse import unquote_to_bytes
        data = unquote_to_bytes(payload)
    return mediatype, data


def extension_for_mime(mime: str) -> str:
    return MIME_EXTENSIONS.get(mime) or mimetypes.guess_extension(mime) or ".bin"


def extract_data_uri(
    uri: str,
    assets_dir: Path,
    relative_assets_dir: str,
    digest_to_name: Dict[str, str],
    stats: Stats,
) -> str:
    mime, data = decode_data_uri(html_lib.unescape(uri))
    digest = hashlib.sha256(data).hexdigest()
    if digest in digest_to_name:
        stats.duplicate_images_reused += 1
        return f"{relative_assets_dir}/{digest_to_name[digest]}"

    ext = extension_for_mime(mime)
    filename = f"image-{digest[:12]}{ext}"
    (assets_dir / filename).write_bytes(data)
    digest_to_name[digest] = filename
    stats.unique_images_written += 1
    return f"{relative_assets_dir}/{filename}"


def dedupe_css_rules(css: str, stats: Stats) -> str:
    if tinycss2 is None:
        return css

    rules = tinycss2.parse_stylesheet(css, skip_whitespace=False, skip_comments=False)
    seen: set[str] = set()
    output: List[str] = []

    for rule in rules:
        serialized = tinycss2.serialize([rule])
        if rule.type in {"qualified-rule", "at-rule"}:
            normalized = re.sub(r"\s+", " ", serialized).strip()
            if normalized in seen:
                stats.duplicate_css_rules_removed += 1
                continue
            seen.add(normalized)
        output.append(serialized)

    return "".join(output)


def optimize(source: Path, output_dir: Path, overwrite: bool = False) -> Tuple[Path, Path, Stats]:
    if output_dir.exists():
        if not overwrite:
            raise FileExistsError(f"Output directory already exists: {output_dir}")
        shutil.rmtree(output_dir)

    output_dir.mkdir(parents=True)
    assets_dir = output_dir / f"{source.stem}-assets"
    assets_dir.mkdir()

    raw_html = source.read_text(encoding="utf-8", errors="strict")
    stats = Stats()
    digest_to_name: Dict[str, str] = {}
    relative_assets_dir = f"/project-assets/{source.stem}-assets"

    # Externalize all inline styles without reparsing/reformatting the document
    style_blocks = STYLE_RE.findall(raw_html)
    stats.style_blocks_externalized = len(style_blocks)
    css = "\n\n/* ---- MATLAB export style block ---- */\n\n".join(style_blocks)
    html_without_styles = STYLE_RE.sub("", raw_html)

    # Extract data images used inside CSS
    def replace_css_image(match: re.Match[str]) -> str:
        stats.css_images_seen += 1
        path = extract_data_uri(
            match.group("data"), assets_dir, relative_assets_dir,
            digest_to_name, stats,
        )
        return f'url("{path}")'

    css = CSS_DATA_IMAGE_RE.sub(replace_css_image, css)
    css = dedupe_css_rules(css, stats)

    css_name = f"{source.stem}.matlab.css"
    css_path = output_dir / css_name
    css_path.write_text(css, encoding="utf-8")

    stylesheet_link = f'\n<link rel="stylesheet" href="/css/{css_name}">\n'
    if HEAD_CLOSE_RE.search(html_without_styles):
        optimized_html = HEAD_CLOSE_RE.sub(stylesheet_link + "</head>", html_without_styles, count=1)
    else:
        optimized_html = stylesheet_link + html_without_styles

    # Extract data images used in HTML attributes
    def replace_html_image(match: re.Match[str]) -> str:
        stats.html_images_seen += 1
        path = extract_data_uri(
            match.group("data"), assets_dir, relative_assets_dir,
            digest_to_name, stats,
        )
        quote = match.group("quote")
        return f"{match.group('prefix')}{quote}{path}{quote}"

    optimized_html = HTML_DATA_IMAGE_RE.sub(replace_html_image, optimized_html)

    html_path = output_dir / source.name
    html_path.write_text(optimized_html, encoding="utf-8")

    report = output_dir / f"{source.stem}-optimization-report.txt"
    original_size = source.stat().st_size
    html_size = html_path.stat().st_size
    css_size = css_path.stat().st_size
    assets_size = sum(p.stat().st_size for p in assets_dir.iterdir() if p.is_file())
    total_size = html_size + css_size + assets_size
    report.write_text(
        "\n".join([
            f"Source: {source}",
            f"Original HTML size: {original_size:,} bytes",
            f"Optimized HTML size: {html_size:,} bytes",
            f"External CSS size: {css_size:,} bytes",
            f"Extracted assets size: {assets_size:,} bytes",
            f"Optimized total size: {total_size:,} bytes",
            f"HTML data images found: {stats.html_images_seen}",
            f"CSS data images found: {stats.css_images_seen}",
            f"Unique image files written: {stats.unique_images_written}",
            f"Duplicate images reused: {stats.duplicate_images_reused}",
            f"Style blocks externalized: {stats.style_blocks_externalized}",
            f"Exact duplicate CSS rules removed: {stats.duplicate_css_rules_removed}",
        ]) + "\n",
        encoding="utf-8",
    )

    return html_path, report, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="MATLAB-exported HTML file")
    parser.add_argument("-o", "--output-dir", type=Path, help="Output directory")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output directory")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error(f"File not found: {source}")

    output_dir = args.output_dir
    if output_dir is None:
        output_dir = source.with_name(f"{source.stem}-optimized")
    output_dir = output_dir.expanduser().resolve()

    try:
        html_path, report, stats = optimize(source, output_dir, args.overwrite)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Optimized HTML: {html_path}")
    print(f"Report:         {report}")
    print(f"Images written: {stats.unique_images_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
