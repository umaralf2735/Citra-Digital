# image_processor.py
import cv2
import numpy as np

def to_grayscale(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)  # keep 3-channel
    return img

def invert(img):
    return cv2.bitwise_not(img)

def adjust_brightness_contrast(img, brightness=0, contrast=1.0):
    return cv2.convertScaleAbs(img, alpha=contrast, beta=brightness)

def histogram_equalization(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eq = cv2.equalizeHist(gray)
    return cv2.cvtColor(eq, cv2.COLOR_GRAY2BGR)

def apply_filter(img, filter_type='mean'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if filter_type == 'mean':
        filtered = cv2.blur(gray, (5, 5))
    elif filter_type == 'gaussian':
        filtered = cv2.GaussianBlur(gray, (5, 5), 0)
    elif filter_type == 'median':
        filtered = cv2.medianBlur(gray, 5)
    else:
        raise ValueError("Filter tidak dikenali")
    return cv2.cvtColor(filtered, cv2.COLOR_GRAY2BGR)

def edge_detection(img, method='sobel'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if method == 'sobel':
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        edges = np.uint8(np.clip(cv2.magnitude(sobelx, sobely), 0, 255))
    elif method == 'prewitt':
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        imgx = cv2.filter2D(gray, -1, kernelx)
        imgy = cv2.filter2D(gray, -1, kernely)
        edges = np.uint8(np.clip(cv2.magnitude(imgx.astype(np.float64), imgy.astype(np.float64)), 0, 255))
    elif method == 'canny':
        edges = cv2.Canny(gray, 100, 200)
    else:
        raise ValueError("Metode edge detection tidak dikenali")
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)