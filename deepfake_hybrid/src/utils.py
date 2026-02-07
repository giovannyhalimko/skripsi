import os
import json
import yaml
import random
import logging
import hashlib
import socket
from pathlib import Path
from typing import Any, Dict

import numpy as np
import torch


def seed_everything(seed: int = 42, deterministic: bool = True) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    if deterministic:
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def setup_logging(log_path: Path | None = None, level: int = logging.INFO) -> None:
    log_format = "[%(asctime)s] %(levelname)s: %(message)s"
    logging.basicConfig(level=level, format=log_format)
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)


def load_config(path: str | Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_json(obj: Dict[str, Any], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def hash_string(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def worker_init_fn(worker_id: int) -> None:
    seed = torch.initial_seed() % 2**32
    np.random.seed(seed + worker_id)
    random.seed(seed + worker_id)


def get_num_workers(cfg: Dict[str, Any]) -> int:
    return int(cfg.get("num_workers", os.cpu_count() or 4))


def env_info() -> Dict[str, Any]:
    return {
        "hostname": socket.gethostname(),
        "cuda": torch.cuda.is_available(),
        "num_gpus": torch.cuda.device_count(),
        "torch_version": torch.__version__,
    }
