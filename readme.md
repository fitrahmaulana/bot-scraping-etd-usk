# Web Scraper Dokumen ETD Universitas Syiah Kuala

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

Sebuah aplikasi web sederhana yang dibangun dengan Python dan Flask untuk mengotomatisasi proses pengunduhan dokumen dari portal ETD (Electronic Theses and Dissertations) Universitas Syiah Kuala. Aplikasi ini mengambil setiap halaman gambar dari sebuah dokumen, lalu menggabungkannya menjadi satu file `.zip` yang mudah diakses.

## Tampilan Aplikasi

![Screenshot Aplikasi](https://raw.githubusercontent.com/fitrahmaulana/bot-scraping-etd-usk/refs/heads/main/tampilan%20web%20scraper.png)

## Fitur Utama

-   **Antarmuka Web Sederhana:** Tidak perlu menjalankan skrip dari terminal yang rumit, cukup buka browser.
-   **Log Proses Real-time:** Pantau kemajuan unduhan secara langsung melalui kotak log di browser.
-   **Riwayat Unduhan:** Lihat daftar semua dokumen yang pernah Anda unduh, lengkap dengan link untuk mengunduhnya kembali.
-   **Lintas Platform:** Dapat dijalankan di Windows, macOS, dan Linux.

## Teknologi yang Digunakan

-   **Backend:** Python, Flask, Requests, BeautifulSoup4
-   **Frontend:** HTML, CSS, JavaScript (Server-Sent Events untuk komunikasi real-time)

---

## Instalasi & Persiapan

Ikuti langkah-langkah ini untuk menjalankan aplikasi di komputer Anda.

#### 1. Prasyarat

-   Pastikan Anda sudah menginstall **Python 3** ([unduh di sini](https://www.python.org/downloads/)).
-   Pastikan Anda sudah menginstall **Git** ([unduh di sini](https://git-scm.com/)).

#### 2. Klon Repositori

Buka Terminal atau Command Prompt, lalu klon repositori ini:

```bash
git clone https://github.com/fitrahmaulana/bot-scraping-etd-usk.git
cd bot-scraping-etd-usk
````

#### 3\. Install Kebutuhan (Dependencies)



Install semua library tersebut dengan satu perintah:

```bash
pip install -r requirements.txt
```

-----

## Cara Menjalankan Aplikasi

1.  Pastikan Anda berada di direktori utama proyek.
2.  Jalankan aplikasi dengan perintah:
    ```bash
    python app.py
    ```
3.  Server akan berjalan. Buka browser web Anda dan kunjungi alamat:
    **[http://127.0.0.1:5000](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:5000)**

## Cara Menggunakan (Panduan Bergambar)

Aplikasi ini dirancang agar mudah digunakan. Ikuti 4 langkah mudah ini.

#### Langkah 1: Buka Halaman Dokumen di Situs ETD

Buka browser Anda dan cari dokumen yang ingin Anda unduh. Biasanya Anda akan tiba di halaman "Detail Informasi" seperti ini.

#### Langkah 2: Temukan `bacaID` di URL

Lihatlah address bar browser Anda. Nomor yang ada setelah `id=` atau `bacaID=` adalah nomor yang kita butuhkan.
![enter image description here](https://raw.githubusercontent.com/fitrahmaulana/bot-scraping-etd-usk/refs/heads/main/panduan.png)
Pada contoh di atas, URL-nya adalah `...p=show_detail&id=105248`. Jadi, `bacaID`-nya adalah **105248**.

#### Langkah 3: Jalankan Aplikasi & Masukkan `bacaID`

  - Buka tab baru dan pergi ke aplikasi web Anda yang berjalan di `http://127.0.0.1:5000`.
  - Masukkan `bacaID` (**105248**) yang sudah Anda temukan ke dalam kolom input.
  - Klik tombol **"Mulai Unduh"**.

#### Langkah 4: Pantau Proses dan Unduh Hasilnya

  - Perhatikan log proses yang berjalan secara real-time.
  - Setelah selesai, sebuah link "Klik di sini untuk memuat ulang..." akan muncul. Klik link tersebut.
  - File ZIP baru Anda akan tersedia di bagian paling atas daftar "Riwayat Unduhan". Klik nama filenya untuk mengunduh.

## Cara Menghentikan Aplikasi

Untuk menghentikan server, kembali ke jendela Terminal/Command Prompt tempat aplikasi berjalan, lalu tekan **`Ctrl + C`**.

## Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](https://www.google.com/search?q=LICENSE).

## Kredit

Aplikasi ini dikonsep dan dibuat oleh:
**Fitrah Maulana** - Ilmu Pemerintahan, Universitas Syiah Kuala.