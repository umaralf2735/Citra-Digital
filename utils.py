
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_histogram_to_tkinter(img, parent_widget, canvas_ref):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(gray.ravel(), bins=256, range=[0, 256], color='steelblue', alpha=0.7)
    ax.set_title("Histogram Citra", fontsize=12)
    ax.set_xlabel("Intensitas")
    ax.set_ylabel("Frekuensi")
    ax.grid(True, linestyle='--', alpha=0.5)

    if canvas_ref and canvas_ref.get_tk_widget():
        canvas_ref.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=parent_widget)
    canvas.draw()
    return canvas