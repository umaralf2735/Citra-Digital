const fileInput = document.getElementById('fileInput');
const mainImage = document.getElementById('mainImage');
const placeholder = document.querySelector('.placeholder-text');
const loader = document.getElementById('loader');
const toolsSection = document.getElementById('tools');

let originalImageBlob = null;
let currentImageBlob = null;

// Handle file upload
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        originalImageBlob = file;
        currentImageBlob = file;
        displayImage(file);
        
        // Enable tools
        toolsSection.style.opacity = '1';
        toolsSection.style.pointerEvents = 'auto';
        
        // Reset sliders
        document.getElementById('brightness').value = 0;
        document.getElementById('contrast').value = 1.0;
        document.getElementById('val-b').innerText = '0';
        document.getElementById('val-c').innerText = '1.0';
    }
});

function displayImage(blob) {
    const url = URL.createObjectURL(blob);
    mainImage.src = url;
    mainImage.style.display = 'block';
    placeholder.style.display = 'none';
}

// Reset button
document.getElementById('resetBtn').addEventListener('click', () => {
    if (!originalImageBlob) return alert("Pilih gambar terlebih dahulu!");
    currentImageBlob = originalImageBlob;
    displayImage(originalImageBlob);
    
    document.getElementById('brightness').value = 0;
    document.getElementById('contrast').value = 1.0;
    document.getElementById('val-b').innerText = '0';
    document.getElementById('val-c').innerText = '1.0';
});

// Download button
document.getElementById('downloadBtn').addEventListener('click', () => {
    if (!currentImageBlob) return alert("Tidak ada gambar untuk disimpan.");
    const url = URL.createObjectURL(currentImageBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'mini_photoshop_web.jpg';
    a.click();
    URL.revokeObjectURL(url);
});

// Update slider values dynamically
document.getElementById('brightness').addEventListener('input', e => document.getElementById('val-b').innerText = e.target.value);
document.getElementById('contrast').addEventListener('input', e => document.getElementById('val-c').innerText = e.target.value);

// API call helper
async function processImage(action, param = null) {
    if (!currentImageBlob) return alert("Muat gambar dulu bang!");
    
    loader.style.display = 'flex';
    const formData = new FormData();
    
    // Kirim gambar yang sedang aktif
    formData.append('image', currentImageBlob); 
    formData.append('action', action);
    if (param) formData.append('param', param);

    if (action === 'brightness_contrast') {
        // Brightness & Contrast sebaiknya dieksekusi dari gambar aslinya (agar tidak compounding ekstrem berulang-ulang),
        // tapi di web app ini kita biarkan compounding per klik "Terapkan" seperti layer adjustment.
        formData.append('brightness', document.getElementById('brightness').value);
        formData.append('contrast', document.getElementById('contrast').value);
    }

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.error || "Gagal memproses gambar di server.");
        }
        
        const blob = await response.blob();
        currentImageBlob = blob;
        displayImage(blob);
        
    } catch (err) {
        alert("Error: " + err.message);
    } finally {
        loader.style.display = 'none';
    }
}

// Bind all tool buttons
document.querySelectorAll('.btn-tool').forEach(btn => {
    btn.addEventListener('click', () => {
        const action = btn.dataset.action;
        const param = btn.dataset.param;
        processImage(action, param);
    });
});

// Apply Brightness/Contrast specifically
document.getElementById('applyBC').addEventListener('click', () => {
    processImage('brightness_contrast');
});
