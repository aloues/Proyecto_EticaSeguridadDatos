import logging
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import pandas as pd

# Configuración del logging
logging.basicConfig(filename='data_security.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def encrypt(data, key):
    """ Encripta datos usando AES-256 y guarda el resultado en un CSV. """
    cipher = AES.new(key, AES.MODE_CBC)  # AES requiere un IV
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    encrypted_data = iv + ":" + ct

    # Crea un DataFrame y guarda el dato encriptado
    df = pd.DataFrame({'EncryptedData': [encrypted_data]})
    df.to_csv('encrypted_data.csv', mode='a', header=False, index=False)  # Guarda en CSV sin índice y añade al archivo existente

    return encrypted_data

def decrypt(encrypted_data, key):
    """ Desencripta datos usando AES-256. """
    try:
        iv, ct = encrypted_data.split(':')  # Extraer IV y CT separados por dos puntos
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode()
    except ValueError as e:
        logging.error(f"Error during decryption: {e}")
        return "Error during decryption"

def hash_data(data):
    """ Aplica hashing SHA-256 a los datos. """
    return sha256(data.encode()).hexdigest()

def log_access(operation, data_type):
    """ Registra las operaciones para auditoría. """
    logging.info(f"Operation: {operation}, Data Type: {data_type}")

key = b'1234567890123456' 

# Ejemplo de uso:
if __name__ == "__main__":
    original_data = 'example@example.com'
    encrypted = encrypt(original_data, key)
    print("Encrypted:", encrypted)
    decrypted = decrypt(encrypted, key)
    print("Decrypted:", decrypted)
    hashed = hash_data(original_data)
    print("Hashed:", hashed)
    log_access('test', 'email')
