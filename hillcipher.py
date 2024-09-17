# Dzakwan Fadhlullah - 140810220060
import numpy as np

# Fungsi untuk mengonversi huruf menjadi angka (A=0, B=1, ..., Z=25)
def letter_to_num(letter):
    return ord(letter.upper()) - ord('A')

# Fungsi untuk mengonversi angka menjadi huruf (0=A, 1=B, ..., 25=Z)
def num_to_letter(num):
    return chr(num % 26 + ord('A'))

# Fungsi untuk enkripsi menggunakan Hill Cipher
def encrypt(plaintext, key_matrix):
    # Menyesuaikan panjang plaintext sesuai dengan ukuran matriks
    n = key_matrix.shape[0]
    plaintext = plaintext.replace(" ", "").upper()
    
    # Menambahkan 'X' jika panjang plaintext tidak sesuai dengan ukuran matriks
    while len(plaintext) % n != 0:
        plaintext += 'X'
    
    encrypted_text = ''
    
    for i in range(0, len(plaintext), n):
        # Mengonversi blok teks menjadi vektor angka
        block = np.array([letter_to_num(c) for c in plaintext[i:i+n]])
        
        # Mengalikan matriks kunci dengan vektor angka
        cipher_block = np.dot(key_matrix, block) % 26
        
        # Mengonversi kembali hasilnya menjadi huruf
        encrypted_text += ''.join(num_to_letter(num) for num in cipher_block)
    
    return encrypted_text

# Fungsi untuk dekripsi Hill Cipher
def decrypt(ciphertext, key_matrix):
    # Menyesuaikan panjang ciphertext sesuai dengan ukuran matriks
    n = key_matrix.shape[0]
    ciphertext = ciphertext.replace(" ", "").upper()
    
    # Mencari invers dari matriks kunci dalam modulo 26
    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)  # Invers determinan
    adjugate_matrix = np.round(det * np.linalg.inv(key_matrix)).astype(int) % 26
    key_inv = (det_inv * adjugate_matrix) % 26
    
    decrypted_text = ''
    
    for i in range(0, len(ciphertext), n):
        # Mengonversi blok teks menjadi vektor angka
        block = np.array([letter_to_num(c) for c in ciphertext[i:i+n]])
        
        # Mengalikan matriks kunci invers dengan vektor angka
        plain_block = np.dot(key_inv, block) % 26
        
        # Mengonversi kembali hasilnya menjadi huruf
        decrypted_text += ''.join(num_to_letter(num) for num in plain_block)
    
    return decrypted_text

# Fungsi untuk menemukan kunci dari plaintext dan ciphertext
def find_key(plaintext, ciphertext, n):
    # Mengonversi plaintext dan ciphertext menjadi blok vektor
    plaintext_blocks = [np.array([letter_to_num(c) for c in plaintext[i:i+n]]) for i in range(0, len(plaintext), n)]
    ciphertext_blocks = [np.array([letter_to_num(c) for c in ciphertext[i:i+n]]) for i in range(0, len(ciphertext), n)]
    
    # Membuat matriks dari blok plaintext dan ciphertext
    P = np.column_stack(plaintext_blocks)
    C = np.column_stack(ciphertext_blocks)
    
    # Mencari invers dari matriks P
    P_inv = np.linalg.inv(P).astype(int) % 26
    
    # Mencari matriks kunci: K = C * P^(-1)
    key_matrix = np.dot(C, P_inv) % 26
    
    return key_matrix

# Program utama
if __name__ == "__main__":
    choice = input("Pilih operasi (1: Enkripsi, 2: Dekripsi, 3: Temukan Kunci): ")
    
    if choice == '1':
        plaintext = input("Masukkan plaintext: ").upper()
        print("Masukkan matriks kunci (misal: 2x2 atau 3x3):")
        key_matrix = []
        size = int(input("Ukuran matriks (misal: 2 untuk 2x2, 3 untuk 3x3): "))
        for i in range(size):
            row = list(map(int, input(f"Masukkan baris ke-{i+1} matriks (dipisahkan dengan spasi): ").split()))
            key_matrix.append(row)
        key_matrix = np.array(key_matrix)
        print("Ciphertext:", encrypt(plaintext, key_matrix))
    
    elif choice == '2':
        ciphertext = input("Masukkan ciphertext: ").upper()
        print("Masukkan matriks kunci:")
        key_matrix = []
        size = int(input("Ukuran matriks (misal: 2 untuk 2x2, 3 untuk 3x3): "))
        for i in range(size):
            row = list(map(int, input(f"Masukkan baris ke-{i+1} matriks (dipisahkan dengan spasi): ").split()))
            key_matrix.append(row)
        key_matrix = np.array(key_matrix)
        print("Plaintext:", decrypt(ciphertext, key_matrix))
    
    elif choice == '3':
        plaintext = input("Masukkan plaintext: ").upper()
        ciphertext = input("Masukkan ciphertext: ").upper()
        size = int(input("Ukuran matriks kunci (misal: 2 untuk 2x2, 3 untuk 3x3): "))
        print("Matriks kunci yang ditemukan:")
        print(find_key(plaintext, ciphertext, size))
    
    else:
        print("Pilihan tidak valid!")
