import argparse
import os
import sys
import time
import json
import tempfile
import urllib.request
from pathlib import Path
from tqdm import tqdm

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from utils import load_config, ensure_dir

FILELIST_URL = "misc/filelist.json"
DEEPFEAKES_DETECTION_URL = "misc/deepfake_detection_filenames.json"

DATASETS = {
    "original": "original_sequences/youtube",
    "DeepFakeDetection_original": "original_sequences/actors",
    "Deepfakes": "manipulated_sequences/Deepfakes",
    "DeepFakeDetection": "manipulated_sequences/DeepFakeDetection",
    "Face2Face": "manipulated_sequences/Face2Face",
    "FaceShifter": "manipulated_sequences/FaceShifter",
    "FaceSwap": "manipulated_sequences/FaceSwap",
    "NeuralTextures": "manipulated_sequences/NeuralTextures",
}

COMPRESSION = ["raw", "c23", "c40"]
SERVERS = {
    "EU": "http://canis.vc.in.tum.de:8100/",
    "EU2": "http://kaldir.vc.in.tum.de/faceforensics/",
    "CA": "http://falas.cmpt.sfu.ca:8100/",
}


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration + 1e-9))
    percent = int(count * block_size * 100 / total_size) if total_size > 0 else 0
    sys.stdout.write(
        f"\rProgress: {percent}% {progress_size/ (1024*1024):.1f} MB {speed} KB/s {duration:.1f} sec"
    )
    sys.stdout.flush()


def download_file(url: str, out_file: Path, report_progress: bool = False):
    out_file.parent.mkdir(parents=True, exist_ok=True)
    if out_file.exists():
        tqdm.write(f"Skip existing {out_file}")
        return
    fh, tmp = tempfile.mkstemp(dir=out_file.parent)
    os.close(fh)
    tmp_path = Path(tmp)
    try:
        if report_progress:
            urllib.request.urlretrieve(url, tmp_path, reporthook=reporthook)
        else:
            urllib.request.urlretrieve(url, tmp_path)
        tmp_path.rename(out_file)
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)


def load_json_url(url: str):
    return json.loads(urllib.request.urlopen(url).read().decode("utf-8"))


def get_server_urls(server_key: str):
    if server_key not in SERVERS:
        raise ValueError(f"server must be one of {list(SERVERS.keys())}")
    base_server = SERVERS[server_key]
    tos_url = base_server + "webpage/FaceForensics_TOS.pdf"
    base_url = base_server + "v3/"
    deepfakes_model_url = base_server + "v3/manipulated_sequences/Deepfakes/models/"
    return tos_url, base_url, deepfakes_model_url


def download_ffpp(base_url: str, output_root: Path, datasets, compression: str, file_type: str, num_videos: int | None):
    if compression not in COMPRESSION:
        raise ValueError(f"compression must be in {COMPRESSION}")
    # load filelists once
    file_pairs = load_json_url(base_url + FILELIST_URL)
    dfd_list = load_json_url(base_url + DEEPFEAKES_DETECTION_URL)

    for ds_name in datasets:
        ds_path = DATASETS[ds_name]
        print(f"Downloading {file_type} of dataset {ds_name} -> {ds_path}")

        if "DeepFakeDetection" in ds_path or "actors" in ds_path:
            if "actors" in ds_path:
                filelist = dfd_list["actors"]
            else:
                filelist = dfd_list["DeepFakesDetection"]
        elif "original" in ds_path:
            filelist = []
            for pair in file_pairs:
                filelist += pair
        else:
            filelist = []
            for pair in file_pairs:
                filelist.append("_".join(pair))
                if file_type != "models":
                    filelist.append("_".join(pair[::-1]))

        if num_videos is not None and num_videos > 0:
            filelist = filelist[:num_videos]

        ds_videos_url = base_url + f"{ds_path}/{compression}/{file_type}/"
        ds_masks_url = base_url + f"{ds_path}/masks/videos/"

        if file_type == "videos":
            out_path = output_root / ds_path / compression / file_type
            files = [f + ".mp4" for f in filelist]
            for fname in tqdm(files, desc=f"{ds_name}-{file_type}"):
                download_file(ds_videos_url + fname, out_path / fname)
        elif file_type == "masks":
            if "original" in ds_name:
                print("Masks unavailable for original; skipping")
                continue
            if "FaceShifter" in ds_name:
                print("Masks unavailable for FaceShifter; skipping")
                continue
            out_path = output_root / ds_path / file_type / "videos"
            files = [f + ".mp4" for f in filelist]
            for fname in tqdm(files, desc=f"{ds_name}-{file_type}"):
                download_file(ds_masks_url + fname, out_path / fname)
        elif file_type == "models":
            if ds_name != "Deepfakes":
                print("Models only available for Deepfakes; skipping")
                continue
            out_path = output_root / ds_path / file_type
            for folder in tqdm(filelist, desc="Deepfakes-models"):
                for model_name in ["decoder_A.h5", "decoder_B.h5", "encoder.h5"]:
                    url = base_url + f"manipulated_sequences/Deepfakes/models/{folder}/{model_name}"
                    download_file(url, out_path / folder / model_name)
        else:
            raise ValueError("file_type must be videos|masks|models")


def main():
    parser = argparse.ArgumentParser(description="Download FaceForensics++ (FF++) dataset")
    parser.add_argument("--config", required=True)
    parser.add_argument("--datasets", nargs="+", default=list(DATASETS.keys()), help="Datasets to download")
    parser.add_argument("--compression", default="c23", choices=COMPRESSION)
    parser.add_argument("--type", default="videos", choices=["videos", "masks", "models"])
    parser.add_argument("--num-videos", type=int, default=None)
    parser.add_argument("--server", default="EU2", choices=list(SERVERS.keys()))
    args = parser.parse_args()

    cfg = load_config(args.config)
    output_root = Path(cfg["datasets"].get("ffpp", {}).get("root", cfg.get("ffpp_root", "./ffpp")))
    output_root = ensure_dir(output_root)

    tos_url, base_url, _ = get_server_urls(args.server)
    print("By continuing you agree to the FaceForensics++ TOS:")
    print(tos_url)
    input("Press Enter to continue or Ctrl-C to abort...")

    download_ffpp(base_url, output_root, args.datasets, args.compression, args.type, args.num_videos)
    print("Done. Files in", output_root)
    print("Celeb-DF is not publicly auto-downloadable; please place videos under the configured celebdf root.")


if __name__ == "__main__":
    main()
