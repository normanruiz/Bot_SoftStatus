import json
from Crypto.Cipher import AES


def decifrar():
    # Lee archivo key en bytes y lo convierte a string
    with open("support", "rb") as f:
        key = f.read()
    # Importa archivo chain con la configuracion
    file_in = open("chain", "rb")
    nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    # desencriptar
    data = cipher.decrypt_and_verify(ciphertext, tag)
    # genero diccionario
    configure = json.loads(data.decode())
    return configure
