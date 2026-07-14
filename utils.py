import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_histogram_to_tkinter(img, parent_widget, canvas_ref):
    # Set style for dark mode
    plt.style.use('dark_background')
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fig, ax = plt.subplots(figsize=(6, 4), facecolor='#252526')
    ax.set_facecolor('#1e1e1e')
    ax.hist(gray.ravel(), bins=256, range=[0, 256], color='#0e639c', alpha=0.8)
    ax.set_title("Histogram Citra", fontsize=12, color='white', pad=15)
    ax.set_xlabel("Intensitas Piksel", color='#aaaaaa')
    ax.set_ylabel("Frekuensi", color='#aaaaaa')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.tick_params(colors='#aaaaaa')
    
    # Remove top and right borders for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#555555')
    ax.spines['bottom'].set_color('#555555')

    fig.tight_layout()

    if canvas_ref and canvas_ref.get_tk_widget():
        canvas_ref.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=parent_widget)
    canvas.draw()
    return canvas