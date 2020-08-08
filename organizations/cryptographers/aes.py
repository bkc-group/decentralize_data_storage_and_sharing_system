from Crypto.Cipher import AES
import binascii, os
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import  ipfshttpclient
# kdf_salt = get_random_bytes(16)
kdf_salt = b'\x806\x01\x90\x06\x8dC\xcc\xb1\x92\xd8\xc9\xf9\xd9\xd2'




def create_secretkey(passphrase):
    '''
    Create secret key from user's password
    '''
    return PBKDF2(passphrase, kdf_salt)


def encrypt_aes_gcm(message, secret_key):
    '''
    Encrypt message with secret key
    '''

    aes_cipher = AES.new(secret_key, AES.MODE_GCM)
    ciphertext, auth_tag = aes_cipher.encrypt_and_digest(message)
    return (ciphertext, aes_cipher.nonce, auth_tag)


def decrypt_aes_gcm(encrypted_msg, secret_key):
    '''
    Decrypt encrypted message by secret key
    '''

    (ciphertext, nonce, auth_tag) = encrypted_msg
    aesCipher = AES.new(secret_key, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, auth_tag)
    return plaintext



# def main():

#     key = create_secretkey("hihi")
#     msg = "tuan".encode('utf-8')

#     (ciphertext, nonce, auth_tag) = encrypt_aes_gcm(msg,key)
#     print(ciphertext)

#     cid = api.add_str(str(ciphertext))
#     print(cid)

#     get = api.cat(cid)
#     print(get.decode('utf-8'))
    

# main()
