# Dzakwan Fadhlullah - 140810220060
import numpy as np

# Fungsi untuk mengonversi huruf alfabet menjadi angka
def letter_to_num(letter):
    return ord(letter.upper()) - ord('A')

# Fungsi untuk mengonversi angka menjadi huruf alfabet
def num_to_letter(num):
    return chr((num % 26) + ord('A'))

# Prosedur enkripsi menggunakan algoritma Hill Cipher
def encrypt(plain_text, key_matrix):
    # Panjang teks disesuaikan dengan ukuran matriks kunci
    size = key_matrix.shape[0]
    plain_text = plain_text.replace(" ", "").upper()
    
    # Jika panjang teks tidak sesuai dengan matriks, tambahkan karakter pengisi
    while len(plain_text) % size != 0:
        plain_text += 'X'
    
    encrypted_result = ''
    
    for i in range(0, len(plain_text), size):
        # Blok teks dikonversi menjadi vektor angka
        block_vector = np.array([letter_to_num(char) for char in plain_text[i:i+size]])
        
        # Kalikan matriks kunci dengan vektor angka
        cipher_vector = np.dot(key_matrix, block_vector) % 26
        
        # Konversi hasil menjadi teks
        encrypted_result += ''.join(num_to_letter(num) for num in cipher_vector)
    
    return encrypted_result

# Prosedur dekripsi menggunakan algoritma Hill Cipher
def decrypt(cipher_text, key_matrix):
    # Panjang ciphertext disesuaikan dengan ukuran matriks
    size = key_matrix.shape[0]
    cipher_text = cipher_text.replace(" ", "").upper()
    
    # Hitung invers dari matriks kunci
    determinant = int(round(np.linalg.det(key_matrix)))
    determinant_inv = pow(determinant, -1, 26)  # Invers modulo 26 dari determinan
    adjugate_matrix = np.round(determinant * np.linalg.inv(key_matrix)).astype(int) % 26
    inverse_key_matrix = (determinant_inv * adjugate_matrix) % 26
    
    decrypted_result = ''
    
    for i in range(0, len(cipher_text), size):
        # Blok ciphertext dikonversi menjadi vektor angka
        cipher_vector = np.array([letter_to_num(char) for char in cipher_text[i:i+size]])
        
        # Kalikan matriks invers dengan vektor angka
        plain_vector = np.dot(inverse_key_matrix, cipher_vector) % 26
        
        # Konversi hasil menjadi teks
        decrypted_result += ''.join(num_to_letter(num) for num in plain_vector)
    
    return decrypted_result

# Prosedur untuk menemukan kunci dari plaintext dan ciphertext
def find_key(plain_text, cipher_text, size):
    # Konversi plaintext dan ciphertext menjadi blok vektor angka
    plain_blocks = [np.array([letter_to_num(char) for char in plain_text[i:i+size]]) for i in range(0, len(plain_text), size)]
    cipher_blocks = [np.array([letter_to_num(char) for char in cipher_text[i:i+size]]) for i in range(0, len(cipher_text), size)]
    
    # Bentuk matriks dari blok plaintext dan ciphertext
    P_matrix = np.column_stack(plain_blocks)
    C_matrix = np.column_stack(cipher_blocks)
    
    # Hitung invers matriks plaintext
    P_inv_matrix = np.linalg.inv(P_matrix).astype(int) % 26
    
    # Hitung kunci matriks: K = C * P_inv
    key_matrix = np.dot(C_matrix, P_inv_matrix) % 26
    
    return key_matrix

# Bagian utama program
if __name__ == "__main__":
    operation = input("Pilih operasi (1: Enkripsi, 2: Dekripsi, 3: Temukan Kunci): ")
    
    if operation == '1':
        plain_text = input("Masukkan plaintext: ").upper()
        print("Masukkan matriks kunci (contoh: 2x2 atau 3x3):")
        key_matrix = []
        matrix_size = int(input("Ukuran matriks (contoh: 2 untuk 2x2, 3 untuk 3x3): "))
        for i in range(matrix_size):
            row = list(map(int, input(f"Masukkan baris ke-{i+1} matriks (pisahkan dengan spasi): ").split()))
            key_matrix.append(row)
        key_matrix = np.array(key_matrix)
        print("Ciphertext:", encrypt(plain_text, key_matrix))
    
    elif operation == '2':
        cipher_text = input("Masukkan ciphertext: ").upper()
        print("Masukkan matriks kunci:")
        key_matrix = []
        matrix_size = int(input("Ukuran matriks (contoh: 2 untuk 2x2, 3 untuk 3x3): "))
        for i in range(matrix_size):
            row = list(map(int, input(f"Masukkan baris ke-{i+1} matriks (pisahkan dengan spasi): ").split()))
            key_matrix.append(row)
        key_matrix = np.array(key_matrix)
        print("Plaintext:", decrypt(cipher_text, key_matrix))
    
    elif operation == '3':
        plain_text = input("Masukkan plaintext: ").upper()
        cipher_text = input("Masukkan ciphertext: ").upper()
        matrix_size = int(input("Ukuran matriks kunci (contoh: 2 untuk 2x2, 3 untuk 3x3): "))
        print("Matriks kunci yang ditemukan:")
        print(find_key(plain_text, cipher_text, matrix_size))
    
    else:
        print("Pilihan tidak valid!")
