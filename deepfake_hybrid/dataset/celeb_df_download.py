#!/usr/bin/env python
"""Download Celeb-DF (v1/v2) assets using a manifest of authorized URLs.

Usage example:
    python celeb_df_download.py ./dataset/celeb_df -m celeb_df_manifest.json --allow-gdrive

Manifest format (JSON):
    [
      {"name": "Celeb-DF-v2.zip", "url": "https://.../your-authorized-link"},
      {"name": "list.zip", "url": "https://.../your-authorized-link"}
    ]
    # or {"files": [...]} wrapper is also accepted.

Notes:
- Celeb-DF distribution requires filling the official request form; this
  script assumes you already obtained download links or Drive IDs from the
  authors or your institution.
- Google Drive links can be fetched with --allow-gdrive when gdown is
  installed (pip install gdown). For other HTTPS links the standard urllib
  path is used.
"""

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.request
from typing import Iterable, List, Mapping

from tqdm import tqdm


start_time = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Celeb-DF files using a JSON manifest of URLs.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "output_path",
        type=str,
        help="Directory where the dataset files will be stored.",
    )
    parser.add_argument(
        "-m",
        "--manifest",
        type=str,
        default="celeb_df_manifest.json",
        help="Path to JSON manifest containing download entries.",
    )
    parser.add_argument(
        "-n",
        "--num_files",
        type=int,
        default=None,
        help="Optional limit on the number of files to download (useful for smoke tests).",
    )
    parser.add_argument(
        "--allow-gdrive",
        action="store_true",
        help="Attempt to use gdown for Google Drive links (requires gdown).",
    )
    return parser.parse_args()


def load_manifest(manifest_path: str) -> List[Mapping[str, str]]:
    if not os.path.isfile(manifest_path):
        raise FileNotFoundError(
            f"Manifest not found: {manifest_path}. Provide a JSON file with name/url entries."
        )
    with open(manifest_path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict) and "files" in data:
        entries = data["files"]
    elif isinstance(data, list):
        entries = data
    else:
        raise ValueError("Manifest must be a list or contain a 'files' key with a list of entries.")

    normalized: List[Mapping[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict) or "url" not in entry or "name" not in entry:
            raise ValueError("Each manifest entry must be a dict with 'name' and 'url' keys.")
        normalized.append({"name": entry["name"], "url": entry["url"]})
    return normalized


def reporthook(count: int, block_size: int, total_size: int) -> None:
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration + 1e-9))
    percent = int(count * block_size * 100 / total_size) if total_size else 0
    sys.stdout.write(
        f"\rProgress: {percent:d}%, {progress_size / (1024 * 1024):.1f} MB, {speed} KB/s, {duration:.1f} s"
    )
    sys.stdout.flush()


def download_with_urllib(url: str, out_file: str) -> None:
    out_dir = os.path.dirname(out_file)
    os.makedirs(out_dir, exist_ok=True)
    fh, tmp_path = tempfile.mkstemp(dir=out_dir)
    os.close(fh)
    try:
        urllib.request.urlretrieve(url, tmp_path, reporthook=reporthook)
        os.replace(tmp_path, out_file)
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def try_download_with_gdown(url: str, out_file: str) -> bool:
    try:
        import gdown  # type: ignore
    except ImportError:
        tqdm.write("gdown not installed; install with `pip install gdown` or omit --allow-gdrive.")
        return False
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    gdown.download(url, out_file, quiet=False)
    return os.path.isfile(out_file)


def download_file(url: str, out_file: str, allow_gdrive: bool = False) -> None:
    if os.path.isfile(out_file):
        tqdm.write(f"Skipping existing file: {out_file}")
        return

    is_gdrive = "drive.google.com" in url or "uc?id=" in url
    if allow_gdrive and is_gdrive:
        success = try_download_with_gdown(url, out_file)
        if success:
            return
        tqdm.write("Falling back to urllib after gdown attempt failed or was unavailable.")

    download_with_urllib(url, out_file)


def main() -> None:
    args = parse_args()
    entries = load_manifest(args.manifest)
    if args.num_files is not None and args.num_files > 0:
        entries = entries[: args.num_files]

    os.makedirs(args.output_path, exist_ok=True)
    tqdm.write("Starting Celeb-DF download. Ensure you have permission to use the provided links.")

    for entry in tqdm(entries, desc="files"):
        destination = os.path.join(args.output_path, entry["name"])
        download_file(entry["url"], destination, allow_gdrive=args.allow_gdrive)

    tqdm.write("Done.")


if __name__ == "__main__":
    main()
