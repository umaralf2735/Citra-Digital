# gui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
from image_processor import *
from utils import plot_histogram_to_tkinter

class MiniPhotoshopGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini Photoshop - Pengolahan Citra Digital")
        self.root.geometry("1200x700")
        self.root.minsize(900, 600)

        self.original_image = None
        self.current_image = None
        self.hist_canvas = None

        self._create_widgets()

    def _create_widgets(self):
        # === Control Panel (kiri) ===
        control = tk.Frame(self.root, width=300, bg="#f5f5f5", relief="groove", bd=1)
        control.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(control, text="🎨 Mini Photoshop", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=10)

        # File ops
        tk.Button(control, text="📂 Load Image", command=self.load_image, width=25).pack(pady=3)
        tk.Button(control, text="💾 Save Image", command=self.save_image, width=25).pack(pady=3)
        tk.Button(control, text="🔄 Reset", command=self.reset, width=25).pack(pady=3)

        ttk.Separator(control, orient='horizontal').pack(fill='x', pady=8)

        # Intensity
        tk.Label(control, text="📊 Intensitas", font=("Arial", 10, "bold"), bg="#f5f5f5").pack()
        tk.Button(control, text="Grayscale", command=self.do_grayscale, width=25).pack(pady=2)
        tk.Button(control, text="Invert", command=self.do_invert, width=25).pack(pady=2)

        self.brightness = tk.IntVar(value=0)
        self.contrast = tk.DoubleVar(value=1.0)
        tk.Label(control, text="Brightness", bg="#f5f5f5").pack()
        tk.Scale(control, from_=-100, to=100, orient=tk.HORIZONTAL,
                 variable=self.brightness, command=self.update_bc).pack()
        tk.Label(control, text="Contrast", bg="#f5f5f5").pack()
        tk.Scale(control, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                 variable=self.contrast, command=self.update_bc).pack()

        ttk.Separator(control, orient='horizontal').pack(fill='x', pady=8)

        # Histogram
        tk.Button(control, text="📈 Histogram", command=self.show_hist, width=25).pack(pady=2)
        tk.Button(control, text="⚖️ Equalization", command=self.do_equalize, width=25).pack(pady=2)

        ttk.Separator(control, orient='horizontal').pack(fill='x', pady=8)

        # Filtering
        tk.Label(control, text="🔧 Filtering", font=("Arial", 10, "bold"), bg="#f5f5f5").pack()
        tk.Button(control, text="Mean Filter", command=lambda: self.apply('filter', 'mean'), width=25).pack(pady=2)
        tk.Button(control, text="Gaussian", command=lambda: self.apply('filter', 'gaussian'), width=25).pack(pady=2)
        tk.Button(control, text="Median", command=lambda: self.apply('filter', 'median'), width=25).pack(pady=2)

        ttk.Separator(control, orient='horizontal').pack(fill='x', pady=8)

        # Edge
        tk.Label(control, text="🔍 Edge Detection", font=("Arial", 10, "bold"), bg="#f5f5f5").pack()
        tk.Button(control, text="Sobel", command=lambda: self.apply('edge', 'sobel'), width=25).pack(pady=2)
        tk.Button(control, text="Prewitt", command=lambda: self.apply('edge', 'prewitt'), width=25).pack(pady=2)
        tk.Button(control, text="Canny", command=lambda: self.apply('edge', 'canny'), width=25).pack(pady=2)

        # === Display Area (kanan) ===
        display = tk.Frame(self.root, bg="white")
        display.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5, pady=5)

        self.img_label = tk.Label(display, text="🖼️ Gambar akan muncul di sini", bg="#e0e0e0", relief="sunken")
        self.img_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # === Callbacks ===
    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.bmp")])
        if path:
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Error", "Gagal membaca gambar!")
                return
            self.original_image = img.copy()
            self.current_image = img.copy()
            self._show_image()
            messagebox.showinfo("✔️", "Gambar berhasil dimuat!")

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("⚠️", "Tidak ada gambar!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.current_image)
            messagebox.showinfo("✔️", "Gambar disimpan!")

    def reset(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
            self._show_image()
            if self.hist_canvas:
                self.hist_canvas.get_tk_widget().destroy()
                self.hist_canvas = None
        else:
            messagebox.showwarning("⚠️", "Belum ada gambar!")

    def _show_image(self):
        if self.current_image is None:
            return
        # Convert BGR → RGB → PIL
        rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        # Resize agar sesuai window
        h = min(pil_img.height, 500)
        ratio = h / pil_img.height
        w = int(pil_img.width * ratio)
        pil_img = pil_img.resize((w, h), Image.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)
        self.img_label.config(image=tk_img, text="")
        self.img_label.image = tk_img  # simpan referensi

    def update_bc(self, _=None):
        if self.current_image is not None:
            b = self.brightness.get()
            c = self.contrast.get()
            self.current_image = adjust_brightness_contrast(self.current_image, b, c)
            self._show_image()

    # --- Actions ---
    def do_grayscale(self):
        if self.current_image is not None:
            self.current_image = to_grayscale(self.current_image)
            self._show_image()

    def do_invert(self):
        if self.current_image is not None:
            self.current_image = invert(self.current_image)
            self._show_image()

    def do_equalize(self):
        if self.current_image is not None:
            self.current_image = histogram_equalization(self.current_image)
            self._show_image()

    def show_hist(self):
        if self.current_image is not None:
            self.hist_canvas = plot_histogram_to_tkinter(
                self.current_image, self.img_label.master, self.hist_canvas
            )
            self.hist_canvas.get_tk_widget().pack(pady=5)

    def apply(self, op_type, param):
        if self.current_image is None:
            messagebox.showwarning("⚠️", "Muat gambar dulu!")
            return
        try:
            if op_type == 'filter':
                self.current_image = apply_filter(self.current_image, param)
            elif op_type == 'edge':
                self.current_image = edge_detection(self.current_image, param)
            self._show_image()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Gagal: {str(e)}")