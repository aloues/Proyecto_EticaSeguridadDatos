import logging
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import random

# Configuración del logging
logging.basicConfig(filename='data_security.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Clave de cifrado (debe ser secreta en producción)
key = b'1234567890123456'

def encrypt(data):
    """ Encripta datos usando AES-256. """
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    encrypted_data = iv + ":" + ct
    return encrypted_data

def decrypt(encrypted_data):
    """ Desencripta datos usando AES-256. """
    try:
        iv, ct = encrypted_data.split(':')
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

def send_2fa_code(email):
    """ Simula el envío de un código de autenticación de dos factores. """
    code = str(random.randint(100000, 999999))  # Código de 6 dígitos
    # En un sistema real, el código se enviaría al correo del usuario.
    print(f"Código 2FA enviado a {email}: {code}")
    return code

def authenticate_user(df, customer_id, password, role):
    """ Autentica al usuario normal o administrador según el rol """
    user_data = df[(df['ID'] == customer_id) & (df['RolAcceso'] == role)]
    if not user_data.empty:
        stored_password = user_data.iloc[0].get('Password')
        if hash_data(password) == stored_password:
            return user_data.iloc[0]
    return None
