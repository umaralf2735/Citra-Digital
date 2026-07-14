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
        self.root.geometry("1200x750")
        self.root.minsize(1000, 700)
        
        # Dark Mode Color Palette
        self.bg_color = "#1e1e1e"
        self.sidebar_color = "#252526"
        self.fg_color = "#ffffff"
        self.btn_color = "#0e639c"
        self.btn_hover = "#1177bb"
        self.accent_color = "#333333"
        
        self.root.configure(bg=self.bg_color)

        self.source_image = None
        self.original_image = None
        self.current_image = None
        self.hist_canvas = None

        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure TSeparator & TScale for dark mode
        style.configure("TSeparator", background=self.accent_color)
        style.configure("Horizontal.TScale", background=self.sidebar_color, troughcolor=self.accent_color)

    def _create_widgets(self):
        # Sidebar Control
        control_outer = tk.Frame(self.root, width=320, bg=self.sidebar_color, relief="flat")
        control_outer.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        control_outer.pack_propagate(False)

        # Create Canvas and Scrollbar for scrollable sidebar
        canvas = tk.Canvas(control_outer, bg=self.sidebar_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_outer, orient="vertical", command=canvas.yview)
        
        control_container = tk.Frame(canvas, bg=self.sidebar_color)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Add frame to canvas
        canvas.create_window((0, 0), window=control_container, anchor="nw", width=305)
        
        # Update scrollregion dynamically
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        control_container.bind("<Configure>", on_frame_configure)

        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mousewheel when cursor is over the sidebar
        canvas.bind("<Enter>", lambda _: canvas.bind_all("<MouseWheel>", on_mousewheel))
        canvas.bind("<Leave>", lambda _: canvas.unbind_all("<MouseWheel>"))

        # Padding container inside scrollable frame
        inner_container = tk.Frame(control_container, bg=self.sidebar_color)
        inner_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=20)

        # Title
        tk.Label(inner_container, text="🎨 Mini Photoshop", font=("Segoe UI", 18, "bold"), 
                 bg=self.sidebar_color, fg=self.fg_color).pack(pady=(0, 15))

        # Main Actions
        self._create_button(inner_container, "📂 Load Image", self.load_image).pack(fill=tk.X, pady=4)
        self._create_button(inner_container, "💾 Save Image", self.save_image).pack(fill=tk.X, pady=4)
        self._create_button(inner_container, "🔄 Reset", self.reset, bg_color="#c9302c", hover_color="#d9534f").pack(fill=tk.X, pady=4)

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)
        
        # Tools: Intensitas
        tk.Label(inner_container, text="⚙️ Intensitas", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        
        btn_frame1 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame1.pack(fill=tk.X)
        self._create_button(btn_frame1, "Grayscale", self.do_grayscale, bg_color=self.accent_color, hover_color="#444").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame1, "Invert", self.do_invert, bg_color=self.accent_color, hover_color="#444").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        # Brightness & Contrast
        tk.Label(inner_container, text="Brightness", bg=self.sidebar_color, fg=self.fg_color, font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
        self.brightness = tk.IntVar(value=0)
        ttk.Scale(inner_container, from_=-100, to=100, orient=tk.HORIZONTAL, 
                  variable=self.brightness, command=self.update_bc, style="Horizontal.TScale").pack(fill=tk.X)
        
        tk.Label(inner_container, text="Contrast", bg=self.sidebar_color, fg=self.fg_color, font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 0))
        self.contrast = tk.DoubleVar(value=1.0)
        ttk.Scale(inner_container, from_=0.1, to=3.0, orient=tk.HORIZONTAL, 
                  variable=self.contrast, command=self.update_bc, style="Horizontal.TScale").pack(fill=tk.X)

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Histogram & EQ
        tk.Label(inner_container, text="📊 Analisis & Enhancements", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame2 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame2.pack(fill=tk.X)
        self._create_button(btn_frame2, "Histogram", self.show_hist, bg_color="#008CBA", hover_color="#007399").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame2, "Equalize", self.do_equalize, bg_color="#008CBA", hover_color="#007399").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Filtering
        tk.Label(inner_container, text="🔍 Filtering", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame3 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame3.pack(fill=tk.X)
        self._create_button(btn_frame3, "Mean", lambda: self.apply('filter', 'mean'), bg_color=self.accent_color, hover_color="#444").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame3, "Gaussian", lambda: self.apply('filter', 'gaussian'), bg_color=self.accent_color, hover_color="#444").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame3, "Median", lambda: self.apply('filter', 'median'), bg_color=self.accent_color, hover_color="#444").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Edge Detection
        tk.Label(inner_container, text="📐 Edge Detection", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame4 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame4.pack(fill=tk.X)
        self._create_button(btn_frame4, "Sobel", lambda: self.apply('edge', 'sobel'), bg_color="#e67e22", hover_color="#d35400").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame4, "Prewitt", lambda: self.apply('edge', 'prewitt'), bg_color="#e67e22", hover_color="#d35400").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame4, "Canny", lambda: self.apply('edge', 'canny'), bg_color="#e67e22", hover_color="#d35400").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Creative Filters
        tk.Label(inner_container, text="🎭 Creative Filters", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame5 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame5.pack(fill=tk.X)
        self._create_button(btn_frame5, "Cartoon", lambda: self.apply_creative('cartoon'), bg_color="#8e44ad", hover_color="#732d91").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame5, "Sketch", lambda: self.apply_creative('sketch'), bg_color="#8e44ad", hover_color="#732d91").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame5, "Sepia", lambda: self.apply_creative('sepia'), bg_color="#8e44ad", hover_color="#732d91").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Transformasi
        tk.Label(inner_container, text="🔄 Transformasi", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame6 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame6.pack(fill=tk.X)
        self._create_button(btn_frame6, "Rot Kiri", lambda: self.apply_transform('ccw'), bg_color="#27ae60", hover_color="#2ecc71").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame6, "Rot Kanan", lambda: self.apply_transform('cw'), bg_color="#27ae60", hover_color="#2ecc71").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame6, "Flip H", lambda: self.apply_transform('h'), bg_color="#27ae60", hover_color="#2ecc71").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame6, "Flip V", lambda: self.apply_transform('v'), bg_color="#27ae60", hover_color="#2ecc71").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        ttk.Separator(inner_container, orient='horizontal').pack(fill='x', pady=15)

        # Tools: Advanced Effects & Noise
        tk.Label(inner_container, text="✨ Advanced & Noise", font=("Segoe UI", 12, "bold"), 
                 bg=self.sidebar_color, fg="#aaaaaa").pack(anchor="w", pady=(5,5))
        btn_frame7 = tk.Frame(inner_container, bg=self.sidebar_color)
        btn_frame7.pack(fill=tk.X)
        self._create_button(btn_frame7, "Sharpen", lambda: self.apply_advanced('sharpen'), bg_color="#c0392b", hover_color="#e74c3c").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 2))
        self._create_button(btn_frame7, "Emboss", lambda: self.apply_advanced('emboss'), bg_color="#c0392b", hover_color="#e74c3c").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame7, "Vignette", lambda: self.apply_advanced('vignette'), bg_color="#c0392b", hover_color="#e74c3c").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 2))
        self._create_button(btn_frame7, "Noise", lambda: self.apply_advanced('noise'), bg_color="#555555", hover_color="#777777").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(2, 0))

        # Main Display Area
        display_container = tk.Frame(self.root, bg=self.bg_color)
        display_container.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Wrapper with border
        img_wrapper = tk.Frame(display_container, bg=self.bg_color, relief="flat", bd=0, highlightbackground="#333", highlightthickness=2)
        img_wrapper.pack(expand=True, fill=tk.BOTH)

        self.img_label = tk.Label(img_wrapper, text="✨ Belum ada gambar yang dimuat.\nSilakan 'Load Image' dari menu di sebelah kiri.", 
                                  font=("Segoe UI", 14), bg=self.bg_color, fg="#777777")
        self.img_label.pack(expand=True, fill=tk.BOTH)

    def _create_button(self, parent, text, command, bg_color=None, hover_color=None):
        if bg_color is None: bg_color = self.btn_color
        if hover_color is None: hover_color = self.btn_hover
        
        btn = tk.Button(parent, text=text, command=command, bg=bg_color, fg=self.fg_color, 
                        font=("Segoe UI", 10, "bold"), relief="flat", bd=0, padx=10, pady=8, cursor="hand2")
        
        # Hover effect events
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))
        return btn

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Error", "Gagal membaca gambar!")
                return
            self.source_image = img.copy()
            self.original_image = img.copy()   
            self.current_image = img.copy()
            
            # Reset scales
            self.brightness.set(0)
            self.contrast.set(1.0)
            
            self._show_image()

    def save_image(self):
        if self.current_image is None:
            messagebox.showwarning("Perhatian", "Tidak ada gambar untuk disimpan!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            cv2.imwrite(path, self.current_image)
            messagebox.showinfo("Sukses", "Gambar berhasil disimpan!")

    def reset(self):
        if self.source_image is not None:
            self.original_image = self.source_image.copy()
            self.current_image = self.source_image.copy()
            self.brightness.set(0)
            self.contrast.set(1.0)
            self._show_image()
            if self.hist_canvas:
                self.hist_canvas.get_tk_widget().destroy()
                self.hist_canvas = None
        else:
            messagebox.showwarning("Perhatian", "Belum ada gambar yang dimuat!")

    def _show_image(self):
        if self.current_image is None:
            return
        rgb = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        
        # Get dynamic max size
        self.root.update_idletasks() 
        max_w = max(self.img_label.winfo_width(), 800)
        max_h = max(self.img_label.winfo_height(), 600)
        
        # Fit within bounding box keeping aspect ratio
        ratio = min(max_w/pil_img.width, max_h/pil_img.height)
        if ratio < 1:
            w = int(pil_img.width * ratio)
            h = int(pil_img.height * ratio)
            pil_img = pil_img.resize((w, h), Image.LANCZOS)
            
        tk_img = ImageTk.PhotoImage(pil_img)
        self.img_label.config(image=tk_img, text="")
        self.img_label.image = tk_img

    def update_bc(self, _=None):
        if self.original_image is None:
            return
        b = self.brightness.get()
        c = self.contrast.get()
        
        temp_img = adjust_brightness_contrast(self.original_image.copy(), b, c)
        self.current_image = temp_img
        self._show_image()

    def do_grayscale(self):
        if self.current_image is not None:
            self.current_image = to_grayscale(self.original_image.copy())
            self._show_image()

    def do_invert(self):
        if self.current_image is not None:
            self.current_image = invert(self.original_image.copy())
            self._show_image()

    def do_equalize(self):
        if self.current_image is not None:
            self.current_image = histogram_equalization(self.original_image.copy())
            self._show_image()

    def show_hist(self):
        if self.current_image is not None:
            hist_window = tk.Toplevel(self.root)
            hist_window.title("Histogram Citra")
            hist_window.geometry("600x450")
            hist_window.configure(bg=self.bg_color)
            
            self.hist_canvas = plot_histogram_to_tkinter(
                self.current_image, hist_window, None
            )
            self.hist_canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def apply(self, op_type, param):
        if self.original_image is None:
            messagebox.showwarning("Perhatian", "Muat gambar terlebih dahulu!")
            return
        try:
            if op_type == 'filter':
                self.current_image = apply_filter(self.original_image.copy(), param)
            elif op_type == 'edge':
                self.current_image = edge_detection(self.original_image.copy(), param)
            self._show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Operasi gagal: {str(e)}")

    def apply_creative(self, effect_name):
        if self.original_image is None:
            messagebox.showwarning("Perhatian", "Muat gambar terlebih dahulu!")
            return
        try:
            if effect_name == 'cartoon':
                self.current_image = cartoon_effect(self.original_image.copy())
            elif effect_name == 'sketch':
                self.current_image = sketch_effect(self.original_image.copy())
            elif effect_name == 'sepia':
                self.current_image = sepia_effect(self.original_image.copy())
            self._show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menerapkan efek: {str(e)}")

    def apply_transform(self, action):
        if self.original_image is None:
            messagebox.showwarning("Perhatian", "Muat gambar terlebih dahulu!")
            return
        try:
            if action in ['cw', 'ccw']:
                self.current_image = rotate_image(self.current_image.copy(), action)
            elif action in ['h', 'v']:
                self.current_image = flip_image(self.current_image.copy(), action)
            self.original_image = self.current_image.copy()
            self._show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menerapkan transformasi: {str(e)}")

    def apply_advanced(self, effect_name):
        if self.original_image is None:
            messagebox.showwarning("Perhatian", "Muat gambar terlebih dahulu!")
            return
        try:
            if effect_name == 'sharpen':
                self.current_image = sharpen_effect(self.original_image.copy())
            elif effect_name == 'emboss':
                self.current_image = emboss_effect(self.original_image.copy())
            elif effect_name == 'vignette':
                self.current_image = vignette_effect(self.original_image.copy())
            elif effect_name == 'noise':
                self.current_image = add_noise(self.original_image.copy())
            self._show_image()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menerapkan efek lanjutan: {str(e)}")