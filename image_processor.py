import cv2
import numpy as np

def to_grayscale(img):
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
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

def cartoon_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def sketch_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inv_gray = cv2.bitwise_not(gray)
    blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
    inv_blur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gray, inv_blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR)

def sepia_effect(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia = cv2.transform(img, kernel)
    return np.clip(sepia, 0, 255).astype(np.uint8)

def rotate_image(img, direction):
    if direction == 'cw':
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif direction == 'ccw':
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img

def flip_image(img, mode):
    if mode == 'h':
        return cv2.flip(img, 1)
    elif mode == 'v':
        return cv2.flip(img, 0)
    return img

def add_noise(img):
    row, col, ch = img.shape
    noisy = np.copy(img)
    amount = 0.02
    num_salt = int(amount * img.size)
    for _ in range(num_salt):
        y = np.random.randint(0, row)
        x = np.random.randint(0, col)
        noisy[y, x] = [255, 255, 255]
    num_pepper = int(amount * img.size)
    for _ in range(num_pepper):
        y = np.random.randint(0, row)
        x = np.random.randint(0, col)
        noisy[y, x] = [0, 0, 0]
    return noisy

def sharpen_effect(img):
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    return cv2.filter2D(img, -1, kernel)

def emboss_effect(img):
    kernel = np.array([[ -2, -1,  0],
                       [ -1,  1,  1],
                       [  0,  1,  2]])
    embossed = cv2.filter2D(img, -1, kernel)
    # OpenCV filter2D can return negative values that wrap. Best to use float then add offset.
    embossed_float = cv2.filter2D(img.astype(np.float32), -1, kernel)
    embossed_float += 128
    return np.clip(embossed_float, 0, 255).astype(np.uint8)

def vignette_effect(img):
    rows, cols = img.shape[:2]
    # generating vignette mask using Gaussian kernels
    kernel_x = cv2.getGaussianKernel(cols, cols/2)
    kernel_y = cv2.getGaussianKernel(rows, rows/2)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    mask = mask / np.max(mask)
    vignette = np.copy(img).astype(np.float32)
    for i in range(3):
        vignette[:,:,i] = vignette[:,:,i] * mask
    return np.clip(vignette, 0, 255).astype(np.uint8)