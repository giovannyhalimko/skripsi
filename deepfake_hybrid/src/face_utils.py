"""Face detection utilities for deepfake detection pipeline."""
from typing import Optional, Tuple

import numpy as np
import cv2


def create_face_detector(device: str = "cpu"):
    """Create an MTCNN face detector configured for speed."""
    from facenet_pytorch import MTCNN
    return MTCNN(
        keep_all=True,
        min_face_size=60,
        thresholds=[0.6, 0.7, 0.7],
        device=device,
        post_process=False,
    )


def detect_face_bbox(
    frame_bgr: np.ndarray,
    detector,
    margin: float = 0.3,
) -> Optional[Tuple[int, int, int, int]]:
    """Detect the largest face and return expanded bbox (x1, y1, x2, y2), or None."""
    h, w = frame_bgr.shape[:2]
    frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

    boxes, _ = detector.detect(frame_rgb)

    if boxes is None or len(boxes) == 0:
        return None

    # Pick the largest face by area
    areas = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    best = int(np.argmax(areas))
    x1, y1, x2, y2 = boxes[best]

    # Expand by margin
    bw, bh = x2 - x1, y2 - y1
    x1 = max(0, int(x1 - bw * margin))
    y1 = max(0, int(y1 - bh * margin))
    x2 = min(w, int(x2 + bw * margin))
    y2 = min(h, int(y2 + bh * margin))

    if x2 - x1 < 10 or y2 - y1 < 10:
        return None

    return (x1, y1, x2, y2)


def crop_face(frame_bgr: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Crop the face region from a BGR frame."""
    x1, y1, x2, y2 = bbox
    return frame_bgr[y1:y2, x1:x2]
