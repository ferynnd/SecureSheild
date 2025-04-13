import os  # Untuk operasi file seperti menghapus file
import base64  # Untuk encode dan decode data biner ke format string
import hashlib  # Untuk membuat hash dari password
from Crypto.Cipher import AES, ChaCha20  # Mengimpor algoritma enkripsi AES dan ChaCha20
from Crypto.Util.Padding import pad, unpad  # Untuk menambahkan dan menghapus padding pada data AES

# Fungsi untuk mengenkripsi teks (misalnya password) menggunakan Vigenere Cipher
def vigenere_encrypt(text, key):
    encrypted_text = ""  # Menyimpan hasil enkripsi sementara
    key_length = len(key)  # Mengambil panjang kunci
    for i in range(len(text)):  # Proses per karakter
        # Menambahkan nilai ASCII karakter teks dan kunci
        encrypted_text += chr((ord(text[i]) + ord(key[i % key_length])) % 256)
    # Encode hasil enkripsi ke base64 agar bisa dijadikan string
    return base64.b64encode(encrypted_text.encode())

# Fungsi untuk mendekripsi Vigenere (opsional, tidak dipakai di versi ini)
def vigenere_decrypt(text, key):
    text = base64.b64decode(text).decode()  # Decode base64
    decrypted_text = ""
    key_length = len(key)
    for i in range(len(text)):
        decrypted_text += chr((ord(text[i]) - ord(key[i % key_length])) % 256)
    return decrypted_text.encode()

# Fungsi untuk mengenkripsi data dengan AES
def aes_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Hash password jadi 32-byte key
    cipher = AES.new(key, AES.MODE_CBC)  # Buat AES cipher dengan mode CBC
    ciphertext = cipher.encrypt(pad(data, AES.block_size))  # Tambah padding dan enkripsi
    # Gabungkan IV dan ciphertext lalu encode ke base64 agar bisa disimpan sebagai string
    return base64.b64encode(cipher.iv + ciphertext).decode()

# Fungsi untuk mendekripsi data dengan AES
def aes_decrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Hash password sama seperti saat enkripsi
    raw_data = base64.b64decode(data)  # Decode dari base64
    iv = raw_data[:16]  # Ambil IV (16 byte pertama)
    ciphertext = raw_data[16:]  # Sisa adalah ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Buat AES cipher dengan IV
    return unpad(cipher.decrypt(ciphertext), AES.block_size)  # Dekripsi dan hapus padding

# Fungsi untuk mengenkripsi data dengan ChaCha20
def chacha_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Hash password jadi key 32 byte
    cipher = ChaCha20.new(key=key)  # Buat cipher ChaCha20
    ciphertext = cipher.encrypt(data)  # Enkripsi data
    return base64.b64encode(cipher.nonce + ciphertext).decode()  # Gabungkan nonce dan ciphertext, lalu encode base64

# Fungsi untuk mendekripsi data dengan ChaCha20
def chacha_decrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Hash password seperti sebelumnya
    raw_data = base64.b64decode(data)  # Decode base64
    nonce = raw_data[:8]  # Ambil nonce (8 byte)
    ciphertext = raw_data[8:]  # Ambil sisa data
    cipher = ChaCha20.new(key=key, nonce=nonce)  # Buat cipher dengan nonce
    return cipher.decrypt(ciphertext)  # Dekripsi data

# Fungsi untuk mengenkripsi file
def encrypt_file(file_path, password):
    # Buka file dan baca dalam mode byte
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    # Transformasi password dengan Vigenere (jadi lebih aman dari password asli)
    transformed_password = vigenere_encrypt(password, 'vig_key').decode()

    # Enkripsi data dengan AES
    aes_ciphertext = aes_encrypt(plaintext, transformed_password)

    # Enkripsi hasil AES lagi dengan ChaCha20
    chacha_ciphertext = chacha_encrypt(aes_ciphertext.encode(), transformed_password)

    # Simpan hasil akhir ke file .enc (hasil dari enkripsi chacha)
    with open(file_path + '.enc', 'w') as f:
        f.write(chacha_ciphertext)

    os.remove(file_path)  # Hapus file asli
    print("File berhasil dienkripsi dan file asli dihapus: " + file_path + '.enc')

# Fungsi untuk mendekripsi file
def decrypt_file(file_path, password):
    # Baca isi file terenkripsi
    with open(file_path, 'r') as f:
        chacha_ciphertext = f.read()

    # Transformasi password dengan Vigenere (harus sama persis dengan saat enkripsi)
    transformed_password = vigenere_encrypt(password, 'vig_key').decode()

    # Dekripsi dari ChaCha → hasilnya adalah ciphertext AES
    aes_ciphertext = chacha_decrypt(chacha_ciphertext, transformed_password).decode()

    # Dekripsi AES → hasil akhirnya adalah data asli
    plaintext = aes_decrypt(aes_ciphertext, transformed_password)

    # Simpan data asli ke file baru (dengan nama sama seperti file awal)
    original_path = file_path.replace('.enc', '')
    with open(original_path, 'wb') as f:
        f.write(plaintext)

    os.remove(file_path)  # Hapus file terenkripsi
    print("File berhasil didekripsi dan file terenkripsi dihapus: " + original_path)

# Program utama
if __name__ == "__main__":
    # Menampilkan ASCII art logo
    shield_ascii = [
        '''
███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗
██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗  
╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝  
███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
███████╗██╗  ██╗██╗███████╗██╗     ██████╗       
██╔════╝██║  ██║██║██╔════╝██║     ██╔══██╗      
███████╗███████║██║█████╗  ██║     ██║  ██║      
╚════██║██╔══██║██║██╔══╝  ██║     ██║  ██║      
███████║██║  ██║██║███████╗███████╗██████╔╝      
╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═════╝   
by: @ferynnd
        ''',
        '''
Welcome to Shield, a simple file encryption tool!
        '''
    ]

    for line in shield_ascii:
        print(line)  # Tampilkan setiap baris logo

    # Input dari pengguna
    choice = input("Choose Operation (1: Encryption, 2: Decryption):  ")
    file_path = input("Insert path file:  ")
    password = input("Insert password:  ")

    # Pilihan user: Enkripsi atau Dekripsi
    if choice == '1':
        encrypt_file(file_path, password)
    elif choice == '2':
        decrypt_file(file_path, password)
    else:
        print("Pilihan tidak valid!")  # Jika input bukan 1/2
