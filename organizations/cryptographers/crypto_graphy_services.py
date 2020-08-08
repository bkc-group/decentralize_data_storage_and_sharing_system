"""
  Author:  BK Blockchain
  Project: ipfs_service
  Created: 09/22/19 10:13
  Purpose: CRYPTO GRAPHY SERVICE SCRIPT FOR IPFS SERVICE PROJECT
"""

from Crypto.Cipher import AES
import binascii, os
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import json 
import ast 
import base64
  


from charm.toolbox.pairinggroup import *
from charm.toolbox.secretutil import SecretUtil
from charm.toolbox.ABEnc import *
from charm.adapters.abenc_adapt_hybrid import HybridABEnc
from charm.core.engine.util import objectToBytes, bytesToObject


# type annotations
pk_t = { 'g':G1, 'g2':G2, 'h':G1, 'f':G1, 'e_gg_alpha':GT }
mk_t = {'beta':ZR, 'g2_alpha':G2 }
sk_t = { 'D':G2, 'Dj':G2, 'Djp':G1, 'S':str }
ct_t = { 'C_tilde':GT, 'C':G1, 'Cy':G1, 'Cyp':G2 }

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





class CPabe_BSW07(ABEnc):
    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group
        util = SecretUtil(groupObj, verbose=False)
        group = groupObj

    # @output(pk_t, mk_t)    
    def setup(self):
        g, gp = group.random(G1), group.random(G2)
        alpha, beta = group.random(), group.random()

        h = g ** beta; f = g ** ~beta
        e_gg_alpha = pair(g, gp ** alpha)
        
        pk = { 'g':g, 'g2':gp, 'h':h, 'f':f, 'e_gg_alpha':e_gg_alpha }
        mk = {'beta':beta, 'g2_alpha':gp ** alpha }
        return (pk, mk)
    
    # @input(pk_t, mk_t, [str])
    # @output(sk_t)
    def keygen(self, pk, mk, S):
        r = group.random() 
        g_r = (pk['g2'] ** r)    
        D = (mk['g2_alpha'] * g_r) ** (1 / mk['beta'])        
        D_j, D_j_pr = {}, {}
        for j in S:
            r_j = group.random()
            D_j[j] = g_r * (group.hash(j, G2) ** r_j)
            D_j_pr[j] = pk['g'] ** r_j
        return { 'D':D, 'Dj':D_j, 'Djp':D_j_pr, 'S':S }
    
    # @input(pk_t, GT, str)
    # @output(ct_t)
    def encrypt(self, pk, M, policy_str):
        print("ma hoa") 
        policy = util.createPolicy(policy_str)
        a_list = util.getAttributeList(policy)
        s = group.random()
        shares = util.calculateSharesDict(s, policy)      

        C = pk['h'] ** s
        C_y, C_y_pr = {}, {}
        for i in shares.keys():
            j = util.strip_index(i)
            C_y[i] = pk['g'] ** shares[i]
            C_y_pr[i] = group.hash(j, G2) ** shares[i] 
        
        C_tilde = (pk['e_gg_alpha'] ** s) * M
        C = C
        Cy = C_y
        Cyp = C_y_pr
        policy = policy_str
        attributes = a_list
        # return (pk['e_gg_alpha'] ** s) * M
       
        return { 'C_tilde':(pk['e_gg_alpha'] ** s) * M,
                 'C':C, 'Cy':C_y, 'Cyp':C_y_pr, 'policy':policy_str, 'attributes':a_list }
    
    # @input(pk_t, sk_t, ct_t)
    # @output(GT)
    def decrypt(self, pk, sk, ct):
        print("decode")
        policy = util.createPolicy(ct['policy'])
        pruned_list = util.prune(policy, sk['S'])
        z = util.getCoefficients(policy)

        A = group.init(GT, 1) 
        for i in pruned_list:
            j = i.getAttributeAndIndex(); k = i.getAttribute()
            A *= ( pair(ct['Cy'][j], sk['Dj'][k]) / pair(sk['Djp'][k], ct['Cyp'][j]) ) ** z[j]

        return ct['C_tilde'] / (pair(ct['C'], sk['D']) / A)
    
def initABE():
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    abe = HybridABEnc(cpabe, groupObj)
    return abe

def create_pk_mk_ABE():
    abe = initABE()
    (pk,mk) = abe.setup()
    return (pk,mk)

def convert(lst):
    return ' or '.join(lst) 

def create_policy_ABE(attrs):
    # access_policy = array_attrs + 'or'+'('+ attrs + ')' 
    access_policy = convert(attrs)
    policy = '(' + access_policy + ')'
    return policy
# def init_policy_ABE(attrs):

def encryptABE(abe,pk, rand_msg, policy_str):
    ct = abe.encrypt(pk, rand_msg, policy_str)
    emsg = objectToBytes(ct,group)
    return emsg

def decryptABE(abe,pk, sk2, ct):
    data = bytesToObject(ct, group)
    msg = abe.decrypt(pk, sk2, data)
    return msg


def dict_to_binary(the_dict):
    str = json.dumps(the_dict)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary


def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)  
    return d
def main():
    abe = initABE()
    (pk,mk) = create_pk_mk_ABE()

    # print(abe)
    # attrs1 = ['TUAN']
    # attrs2 = ['TUAN']
    
    
    # # print(type(attrs1))
    # access_policy = '((four or three) and (three or one))'
    
    # policy = create_policy_ABE(attrs1)
    # print(type(access_policy))
    # print(type(policy))

    # # policy = '((tuan) or (canhtuan))'
    # print("Attributes =>", attrs1); print("Policy =>", access_policy)
    
    
    # sk1 = abe.keygen(pk, mk, attrs1)

    # sk2 = abe.keygen(pk, mk, attrs2)
    
    # # print("day la sk1",sk1)             
    # # print("day la sk2",sk2)             
    # rand_msg = 'Tran canh tuuan'.encode('utf-8')
    # print(type(rand_msg))
    # print("msg =>", rand_msg)
    # ct = encryptABE(abe,pk, rand_msg, policy)
    # print(type(ct))
    
    # print(ct)
   
    # with open("encrypted_data_path.txt", 'wb') as f:
    #     f.write((ct))

    # kiki = open('encrypted_data_path.txt', 'rb').read()
    # print(kiki)
    # data = bytesToObject(kiki, group)
    # plaintext = decryptABE(abe,pk, sk2, data)
    # print(plaintext)

    msg = "chan doi"
    username = 'canhtuan'
    attrs = [username.upper()]
    print(attrs)
    sk = abe.keygen(pk, mk, attrs)
    create_policy = create_policy_ABE(attrs)
    print(create_policy)
    encrypted_content_abe = encryptABE(abe,pk, msg, create_policy)
    print(encrypted_content_abe)

    
    with open('dm.txt', 'wb') as f:
        f.write((encrypted_content_abe))
    
    # encrypt_content_cid_abe = api.add(encrypted_data_path_abe)['Hash']
    # print(encrypt_content_cid_abe)

    ct = open('dm.txt', 'rb').read()
    print(ct)


    # data = bytesToObject(kiki, group)
    plaintext = decryptABE(abe,pk, sk, ct)
    print(plaintext)
    
if __name__ == "__main__":
    main()