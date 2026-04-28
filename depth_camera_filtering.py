import numpy as np

try:
    import cv2
except Exception:
    cv2 = None


def filter_depth(depth, blur_type=None):
    depth = np.asarray(depth)
    if depth.ndim != 2:
        depth = depth.reshape(depth.shape[:2])

    if blur_type is None or cv2 is None:
        return depth

    if blur_type == 'median':
        return cv2.medianBlur(depth.astype(np.float32), 5)

    if blur_type == 'gaussian':
        return cv2.GaussianBlur(depth.astype(np.float32), (5, 5), 0)

    return depth
