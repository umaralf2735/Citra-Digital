# 🎨 Mini Photoshop - Pengolahan Citra Digital

Mini Photoshop adalah aplikasi pengolahan citra digital sederhana namun kaya fitur yang dibangun menggunakan Python dan OpenCV. Proyek ini mendukung dua antarmuka (UI) sekaligus:
1. **Desktop App**: Dibangun menggunakan antarmuka grafis Tkinter dengan tema *Dark Mode*.
2. **Web App (Full-Stack)**: Dibangun menggunakan Flask sebagai backend dan Vanilla JS + HTML + CSS (*Glassmorphism Design*) sebagai frontend interaktif.

## ✨ Fitur Utama

- **⚙️ Intensitas & Penyesuaian Dasar**: 
  - Grayscale & Invert
  - Brightness & Contrast (Slider interaktif)
- **📊 Analisis Gambar**: 
  - Histogram (Grafik sebaran piksel)
  - Histogram Equalization (Pemerataan cahaya)
- **🔍 Filtering & Edge Detection**: 
  - Mean, Gaussian, Median Filter
  - Deteksi Tepi (Edge): Sobel, Prewitt, Canny
- **🎭 Creative Filters**: 
  - Cartoon Effect, Pencil Sketch, Sepia
- **🔄 Transformasi**: 
  - Rotate (Kiri/Kanan), Flip (Horizontal/Vertikal)
- **✨ Advanced & Noise**: 
  - Sharpen, Emboss, Vignette, Salt & Pepper Noise Generator

## 🛠️ Persyaratan Instalasi

Pastikan Anda sudah menginstal Python di komputer Anda. Kemudian, instal semua dependensi yang dibutuhkan dengan menjalankan perintah berikut di terminal:

```bash
pip install -r requirements.txt
```

Library yang digunakan meliputi: `opencv-python`, `pillow`, `numpy`, `matplotlib`, `Flask`, dan `flask-cors`.

## 🚀 Cara Menjalankan Aplikasi

Aplikasi ini dapat dijalankan dalam dua mode. Silakan pilih antarmuka yang Anda sukai!

### 1. Menjalankan Versi Desktop (Tkinter)
Untuk membuka aplikasi berbasis jendela (window) desktop standar:
```bash
python main.py
```

### 2. Menjalankan Versi Website (Web App)
Untuk membuka antarmuka website modern berbasis *Glassmorphism*:
1. Jalankan server backend terlebih dahulu:
   ```bash
   python server.py
   ```
2. Buka browser (Chrome/Edge/Firefox) dan kunjungi:
   👉 **http://127.0.0.1:2026**

## 📂 Struktur Direktori Utama

- `main.py` - File utama untuk menjalankan aplikasi Desktop (Tkinter).
- `gui.py` - Berisi logika dan desain UI untuk versi Desktop.
- `server.py` - File utama untuk menjalankan REST API / Backend versi Web (Flask).
- `image_processor.py` - Pusat pemrosesan gambar (berisi semua rumus dan algoritma OpenCV).
- `utils.py` - Fungsi tambahan (seperti plotting grafik Histogram).
- `static/` - Folder berisi file-file Frontend web (`index.html`, `style.css`, `app.js`).

---
*Dibuat untuk keperluan pembelajaran Pengolahan Citra Digital (Semester 3).*
