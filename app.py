import os
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, Response, send_from_directory
import zipfile
import shutil
import re
import json

# Nonaktifkan peringatan karena menggunakan verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Inisialisasi Aplikasi Flask
app = Flask(__name__)

# Folder untuk menyimpan unduhan sementara dan hasil zip
DOWNLOAD_FOLDER = "temp_downloads"
ZIP_FOLDER = "hasil_zip"

# Pastikan folder ada
if not os.path.exists(ZIP_FOLDER):
    os.makedirs(ZIP_FOLDER)

def sanitize_filename(name):
    """Membersihkan string agar aman untuk dijadikan nama file."""
    # Menghapus karakter ilegal
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Mengganti spasi dengan underscore
    name = name.replace(" ", "_")
    # Menghilangkan underscore berlebih
    name = re.sub(r'_+', '_', name)
    return name

def scrape_and_zip(baca_id):
    """Fungsi utama yang melakukan scraping, memberikan feedback, dan membuat zip."""
    
    session_folder = os.path.join(DOWNLOAD_FOLDER, baca_id)
    if os.path.exists(session_folder):
        shutil.rmtree(session_folder)
    os.makedirs(session_folder)

    base_url = f"https://etd.usk.ac.id/index.php?p=baca&bacaID={baca_id}"
    page_1_url = f"{base_url}&page=1"
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    try:
        # --- Dapatkan total halaman dan METADATA (Penulis & Judul) ---
        yield "data: Mengambil detail dokumen...\n\n"
        response = session.get(page_1_url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        author_name = "Unknown_Author" # Nilai default
        zip_basename = f"dokumen_{baca_id}" # Nama default

        # Ambil nama penulis dan judul
        try:
            author_element = soup.select_one('span.access_socialauthors')
            title_element = soup.select_one('span.title')
            
            if author_element and title_element:
                author_name = author_element.text.strip().replace(',', '')
                document_title = title_element.text.strip()
                
                sanitized_author = sanitize_filename(author_name)
                sanitized_title = sanitize_filename(document_title)[:60]
                zip_basename = f"{sanitized_author}_-_{sanitized_title}"
                yield f"data: ✅ Penulis ditemukan: {author_name}\n\n"
            else:
                yield "data: ⚠️ Gagal menemukan penulis/judul. Menggunakan nama default.\n\n"

        except Exception as e:
            yield f"data: ❌ ERROR saat mengambil metadata: {e}. Menggunakan nama default.\n\n"

        zip_filename = f"{zip_basename}.zip"
        yield f"data: Nama file akan menjadi: {zip_filename}\n\n"

        page_options = soup.select('select[name="page"] option')
        if not page_options:
            yield "data: ERROR: Tidak dapat menemukan total halaman. Periksa kembali bacaID.\n\n"
            return
        
        total_pages = int(page_options[-1]['value'])
        yield f"data: Ditemukan {total_pages} halaman. Memulai unduhan...\n\n"
        time.sleep(1)

        # --- Loop untuk mengunduh setiap halaman ---
        for page_num in range(1, total_pages + 1):
            yield f"data: Memproses halaman {page_num} dari {total_pages}...\n\n"
            page_url = f"{base_url}&page={page_num}"
            page_response = session.get(page_url, verify=False)
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            
            image_element = page_soup.select_one('figure center img')
            if image_element and image_element.has_attr('src'):
                image_url = image_element['src']
                image_response = session.get(image_url, verify=False)
                
                file_name = f"halaman_{page_num:03d}.png"
                file_path = os.path.join(session_folder, file_name)
                with open(file_path, 'wb') as f:
                    f.write(image_response.content)
            else:
                yield f"data: WARNING: Gambar tidak ditemukan di halaman {page_num}.\n\n"

            time.sleep(0.5)

        # --- Membuat file ZIP ---
        yield "data: Semua halaman terunduh. Membuat file ZIP...\n\n"
        zip_filepath = os.path.join(ZIP_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for root, _, files in os.walk(session_folder):
                for file in sorted(files):
                    zipf.write(os.path.join(root, file), arcname=file)
        
        yield f"data: SELESAI! File ZIP berhasil dibuat.\n\n"
        
        # Siapkan data yang mau dikirim (nama file) dalam format JSON
        final_data = {"filename": zip_filename}
        # Kirim event dengan format: event: nama_event\n data: data_json\n\n
        yield f"event: end-of-stream\ndata: {json.dumps(final_data)}\n\n"
        
        # Beri jeda singkat untuk memastikan event terkirim sebelum koneksi ditutup
        time.sleep(1)

    except Exception as e:
        yield f"data: TERJADI ERROR: {e}\n\n"
    finally:
        if os.path.exists(session_folder):
            shutil.rmtree(session_folder)


@app.route('/')
def index():
    """Menampilkan halaman utama dan daftar file yang sudah diunduh."""
    downloaded_files = []
    try:
        all_files = [f for f in os.listdir(ZIP_FOLDER) if f.endswith('.zip')]
        downloaded_files = sorted(
            all_files,
            key=lambda f: os.path.getmtime(os.path.join(ZIP_FOLDER, f)),
            reverse=True
        )
    except FileNotFoundError:
        pass
    
    zip_folder_path = os.path.abspath(ZIP_FOLDER)
    return render_template('index.html', downloaded_files=downloaded_files, zip_folder_path=zip_folder_path)


@app.route('/start-download')
def start_download():
    baca_id = request.args.get('bacaID')
    if not baca_id or not baca_id.isdigit():
        return Response("Error: 'bacaID' tidak valid.", mimetype='text/plain')
    
    return Response(scrape_and_zip(baca_id), mimetype='text/event-stream')

@app.route('/download/<filename>')
def download_zip(filename):
    return send_from_directory(ZIP_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)