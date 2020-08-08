from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import tinyec.ec as ec
import  ipfshttpclient
import  ast



def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext

def create_key_ECC():
	privKey = secrets.randbelow(curve.field.n)
	pubKey = privKey * curve.g
	return privKey, pubKey

def convertPublicKey(pubKey):
    return (hex(pubKey.x),hex(pubKey.y))

def convertToPoint(value):
    s = ec.Point(curve, int(value[0],16), int(value[1],16))
    return s
# privKey, pubKey = create_key_ECC()
# # publicKey = ecc_point_to_256_bit_key(pubKey)
# print (privKey)
# print (pubKey)

# print(tuan)
# privKey = 21039675953997752035291827592635718718315330510935166747150936236736373741055

# x = 20800379211712135251770246501863790549467307788510221503045803737510194761538
# y = 2040266308651836549140686810170154144719969483514061804369501263182339375685
# print("----day la x y----------------------------")
# print(hex(x)) 

# msg = "canhtuan".encode('utf-8')
# s = ec.Point(curve, int(hex(x),16), int(hex(y),16))
# print (s)

# ct  = encrypt_ECC(msg,s)
# print(ct)

# data_push_ipfs = [ct[0].hex(),ct[1].hex(),ct[2].hex(),hex(ct[3].x),hex(ct[3].y)]

# print("data_push_ipfs",data_push_ipfs)
# cid = api.add_json(data_push_ipfs)
# print(cid)

# print("test giai ma ------------------------")

# content_from_ipfs = api.cat(cid)

# #  decode byte
# convert_byte_to_hex = content_from_ipfs.decode('utf-8')


# print("convert_byte_to_hex",convert_byte_to_hex)

# convert_to_list = ast.literal_eval(convert_byte_to_hex)

# encrypted_data = bytes.fromhex(convert_to_list[0])
# nonce = bytes.fromhex(convert_to_list[1])
# tag = bytes.fromhex(convert_to_list[2])
# _x = convert_to_list[3]
# _y = convert_to_list[4]
# ciphertextPubKey = ec.Point(curve, int(_x,16), int(_y,16))

# print(ciphertextPubKey)

# encryptedMsgObj1 =(encrypted_data,nonce,tag,ciphertextPubKey)

# decode = decrypt_ECC(encryptedMsgObj1,privKey)
# print(decode)



