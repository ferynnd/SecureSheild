import os  # Mengimpor modul untuk operasi file dan sistem
import base64  # Mengimpor modul untuk encoding dan decoding base64
import hashlib  # Mengimpor modul untuk hashing
from Crypto.Cipher import AES, ChaCha20  # Mengimpor algoritma enkripsi AES dan ChaCha20 dari PyCryptodome
from Crypto.Util.Padding import pad, unpad  # Mengimpor fungsi padding dan unpadding untuk AES

# Fungsi untuk mengenkripsi teks menggunakan Vigenere Cipher
def vigenere_encrypt(text, key):
    encrypted_text = ""  # Variabel untuk menyimpan hasil enkripsi
    key_length = len(key)  # Panjang kunci
    for i in range(len(text)):
        encrypted_text += chr((ord(text[i]) + ord(key[i % key_length])) % 256)  # Melakukan operasi enkripsi karakter per karakter
    return encrypted_text.encode()  # Mengembalikan teks terenkripsi dalam bentuk byte

# Fungsi untuk mendekripsi teks menggunakan Vigenere Cipher
def vigenere_decrypt(text, key):
    decrypted_text = ""  # Variabel untuk menyimpan hasil dekripsi
    key_length = len(key)  # Panjang kunci
    for i in range(len(text)):
        decrypted_text += chr((ord(text[i]) - ord(key[i % key_length])) % 256)  # Melakukan operasi dekripsi karakter per karakter
    return decrypted_text.encode()  # Mengembalikan teks yang telah didekripsi dalam bentuk byte

# Fungsi untuk mengenkripsi data menggunakan AES
def aes_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Menghasilkan kunci AES dari hash SHA-256
    cipher = AES.new(key, AES.MODE_CBC)  # Membuat objek cipher AES dengan mode CBC
    ciphertext = cipher.encrypt(pad(data, AES.block_size))  # Mengenkripsi data dengan padding
    return base64.b64encode(cipher.iv + ciphertext).decode()  # Menggabungkan IV dan ciphertext lalu mengubahnya menjadi string base64

# Fungsi untuk mendekripsi data menggunakan AES
def aes_decrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Menghasilkan kunci AES dari hash SHA-256
    raw_data = base64.b64decode(data)  # Mendekode data dari base64
    iv = raw_data[:16]  # Memisahkan IV dari data terenkripsi
    ciphertext = raw_data[16:]  # Memisahkan ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Membuat objek cipher AES dengan IV
    return unpad(cipher.decrypt(ciphertext), AES.block_size)  # Mendekripsi dan menghapus padding

# Fungsi untuk mengenkripsi data menggunakan ChaCha20
def chacha_encrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Menghasilkan kunci ChaCha20 dari hash SHA-256
    cipher = ChaCha20.new(key=key)  # Membuat objek cipher ChaCha20
    ciphertext = cipher.encrypt(data)  # Mengenkripsi data
    return base64.b64encode(cipher.nonce + ciphertext).decode()  # Menggabungkan nonce dan ciphertext lalu mengubahnya menjadi string base64

# Fungsi untuk mendekripsi data menggunakan ChaCha20
def chacha_decrypt(data, key):
    key = hashlib.sha256(key.encode()).digest()  # Menghasilkan kunci ChaCha20 dari hash SHA-256
    raw_data = base64.b64decode(data)  # Mendekode data dari base64
    nonce = raw_data[:8]  # Memisahkan nonce
    ciphertext = raw_data[8:]  # Memisahkan ciphertext
    cipher = ChaCha20.new(key=key, nonce=nonce)  # Membuat objek cipher ChaCha20 dengan nonce
    return cipher.decrypt(ciphertext)  # Mendekripsi data

# Fungsi untuk mengenkripsi file
def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        plaintext = f.read()  # Membaca isi file dalam bentuk byte
    
    aes_ciphertext = aes_encrypt(plaintext, password)  # Mengenkripsi dengan AES
    vigenere_key = vigenere_encrypt(password, 'vig_key').decode()  # Mengenkripsi password dengan Vigenere Cipher
    chacha_key = chacha_encrypt(vigenere_key.encode(), password)  # Mengenkripsi kunci Vigenere dengan ChaCha20
    chacha_ciphertext = chacha_encrypt(aes_ciphertext.encode(), password)  # Mengenkripsi hasil AES dengan ChaCha20
    
    with open(file_path + '.enc', 'w') as f:
        f.write(chacha_ciphertext + '\n' + chacha_key)  # Menyimpan hasil enkripsi ke dalam file baru
    
    os.remove(file_path)  # Menghapus file asli
    print("File berhasil dienkripsi dan file asli dihapus: " + file_path + '.enc')

# Fungsi untuk mendekripsi file
def decrypt_file(file_path, password):
    with open(file_path, 'r') as f:
        chacha_ciphertext, chacha_key = f.read().split('\n')  # Membaca dan memisahkan data terenkripsi
    
    vigenere_key = chacha_decrypt(chacha_key, password).decode()  # Mendekripsi kunci Vigenere
    aes_ciphertext = chacha_decrypt(chacha_ciphertext, password).decode()  # Mendekripsi hasil ChaCha20 ke AES ciphertext
    plaintext = aes_decrypt(aes_ciphertext, password)  # Mendekripsi data AES
    
    original_path = file_path.replace('.enc', '')  # Menentukan nama file asli
    with open(original_path, 'wb') as f:
        f.write(plaintext)  # Menyimpan hasil dekripsi ke dalam file baru
    
    os.remove(file_path)  # Menghapus file terenkripsi
    print("File berhasil didekripsi dan file terenkripsi dihapus: " + original_path)

# Program utama
if __name__ == "__main__":
    # Menampilkan ASCII art
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
        print(line)  # Menampilkan teks ASCII
    
    choice = input("Choose Operation (1: Encryption, 2: Decryption):  ")  # Meminta pengguna memilih operasi
    file_path = input("Insert path file:  ")  # Meminta pengguna memasukkan path file
    password = input("Insert password:  ")  # Meminta pengguna memasukkan password
    
    if choice == '1':
        encrypt_file(file_path, password)  # Menjalankan enkripsi file
    elif choice == '2':
        decrypt_file(file_path, password)  # Menjalankan dekripsi file
    else:
        print("Pilihan tidak valid!")  # Menampilkan pesan jika pilihan tidak valid
