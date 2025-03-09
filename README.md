# Shield - File Encryption Tool

Shield adalah alat enkripsi file yang mengimplementasikan enkripsi berlapis menggunakan algoritma AES, ChaCha20, dan Vigenere Cipher untuk memberikan perlindungan ekstra terhadap data.

## Fitur

- **Enkripsi file berlapis** dengan kombinasi AES, ChaCha20, dan Vigenere Cipher.
- **Dukungan dekripsi** untuk mengembalikan file terenkripsi ke bentuk aslinya.
- **Otomatis menghapus file asli** setelah dienkripsi untuk meningkatkan keamanan.

## Instalasi

Pastikan Anda memiliki Python 3 dan pustaka berikut yang diperlukan:

```bash
pip install pycryptodome pycipher 
```

## Cara Penggunaan

Jalankan script dengan perintah berikut:

```bash
python shield.py
```

Kemudian ikuti instruksi yang muncul di terminal:

1. Pilih operasi:
   - `1` untuk enkripsi
   - `2` untuk dekripsi
2. Masukkan path file yang ingin dienkripsi atau didekripsi.
3. Masukkan password untuk mengenkripsi atau mendekripsi file.

## Algoritma yang Digunakan

- **AES (Advanced Encryption Standard)**
  - Menggunakan mode **CBC** (Cipher Block Chaining) untuk keamanan lebih baik.
  - Kunci dienkripsi menggunakan SHA-256 sebelum digunakan.
- **ChaCha20**
  - Algoritma stream cipher yang cepat dan aman.
  - Digunakan untuk mengenkripsi hasil AES dan kunci Vigenere.
- **Vigenere Cipher**
  - Digunakan untuk mengenkripsi password sebelum dienkripsi lebih lanjut dengan ChaCha20.

## Contoh Penggunaan

### Enkripsi File

```bash
Choose Operation (1: Encryption, 2: Decryption): 1
Insert path file: /path/to/file.txt
Insert password: mysecurepassword
File berhasil dienkripsi dan file asli dihapus: /path/to/file.txt.enc
```

### Dekripsi File

```bash
Choose Operation (1: Encryption, 2: Decryption): 2
Insert path file: /path/to/file.txt.enc
Insert password: mysecurepassword
File berhasil didekripsi dan file terenkripsi dihapus: /path/to/file.txt
```

## Kontributor

- **@ferynnd** (Pembuat dan Pengembang Utama)

## Lisensi

Proyek ini tersedia di bawah lisensi MIT. Anda bebas menggunakannya dengan tetap memberikan kredit kepada pengembang asli.

