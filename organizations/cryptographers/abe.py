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
import  ipfshttpclient



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


class CPabe_BSW07(ABEnc):
    def __init__(self, groupObj):
        ABEnc.__init__(self)
        global util, group
        util = SecretUtil(groupObj, verbose=False)
        group = groupObj

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
        # print("ma hoa") 
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
    
def init_abe():
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    abe = HybridABEnc(cpabe, groupObj)
    print(abe)
    return (abe)



def create_pk_mk_abe(abe):
    
    (pk,mk) = abe.setup()
    return (pk,mk)


def create_scret_key(abe,pk,mk,attrs):
    sk = abe.keygen(pk, mk, attrs)
    return sk

def create_policy_abe(attrs):
    # access_policy = array_attrs + 'or'+'('+ attrs + ')' 
    access_policy = convert(attrs)
    policy = '(' + access_policy + ')'
    return policy
# def init_policy_ABE(attrs):

def encrypt_abe(abe,pk, rand_msg, policy_str):
    ct = abe.encrypt(pk, rand_msg, policy_str)
    emsg = objectToBytes(ct,group)
    return emsg

def decrypt_abe(abe,pk, sk2, ct):
    data = bytesToObject(ct, group)
    msg = abe.decrypt(pk, sk2, data)
    return msg


    
def convert(lst):
    return ' and '.join(lst)

def readFilePkMk(groupObj):

    f1 = open("private/pk_bytes", "rb")
    f2 = open("private/mk_bytes", "rb")

    pk = f1.read()
    mk = f2.read()

    orig_pk = bytesToObject(pk, groupObj)
    orig_mk = bytesToObject(mk, groupObj)
    f1.close()
    f2.close()
    return(orig_pk,orig_mk)


def main():
    groupObj = PairingGroup('SS512')
    cpabe = CPabe_BSW07(groupObj)
    abe = HybridABEnc(cpabe, groupObj)



    f1 = open("private/pk_bytes", "rb")
    f2 = open("private/mk_bytes", "rb")

    pk = f1.read()
    mk = f2.read()

    orig_pk = bytesToObject(pk, groupObj)
    orig_mk = bytesToObject(mk, groupObj)


    print(orig_pk)
    
    
    # (pk,mk) = create_pk_mk_abe(abe)
  
    
    attrs1 = ['CANHTUAN','DUY','MANH']
    attrs2 = ['CANHTUAN','DUY']
    msg = "canhtuan".encode('utf-8')
    # policy = create_policy_abe(attrs2)
    policy = '(CANHTUAN and DUY and MANH)'
    # print(policy)
    


    sk2 = create_scret_key(abe,orig_pk,orig_mk,attrs1)
    ct = encrypt_abe(abe,orig_pk,"tuan".encode('utf-8'), policy)
    # print(ct)
    ct =b'eJydV9tuFEcQ/ZXVPiXSSpme6Us1Eg+WgRjFxomAkIuj1d5srNjE8S5OiOV/z1TVOTMbnmIeMDs91XU9darmfroK0yeT++nhfHd5td7Y7/l8dbXYbufz/mm6/LTbbKezSX96t7j6uLHTX1OYTZLMJqFpZ5PazCax9gf9Yen6/0v/om31bZ5NpH+qvaiopL5p+oekb0PUP50eJZcxdaFRXb3OrNJBXLFeN6Up+YGJSYfTnNx26Q9jfy9naCsqGuClag1NLxb1Xqh+KgLPQoCYve1PSq+lVn3ofxT6pq5EgdumTo2Uht72YQkdDAGBqN4s8NaC0cg1mCL+thRoM9OhbXBblWs46mLShCZktkR6J27RUqixima2Ka5TCxApZvJNcC0pU5MqaPyfvbXQihpqA293cMqtRLzTXGnEFpt6r0pjYTjZ4RBZ5YSM6lv3RTxCTWi0IsCyFBgtzE2gYbWpPmnBNe5EU+aRZzkAKZn5GWKwgJNb1SyoBk2l1a2DB+5sSxD2l3P47aFvg8P/2yLWEeKli1RiENPqVGTccqw4FTQOPanMhQXK8hHeoSE6rMxWdNPttZXhZeu49ZolgNKhqkjOLqx41EMtgqYvwxGtQUE9tFqaxAgF+ttAlNiCqHVlk6lmNW43hLXOHt8YeEvYN7xY6xi2/jMoNMB1ROY0DeZ3cqXqs5ZSmYC1+uTcdvDq6M3bg1ePrZylVtUa3Sj0S/cZyJ1mEplFKJcc8t5B9ioiU1offSUDA1X0XkHRJIMCtBIabaG43nUWEm8CYSO0gHHHejTwSwCHAiIZ/LTcgk30utUFudezSkGjauNlJUGi2Vo+A8MRxctoamu8ocaZ+A0uEYmRlkRjkEv/Kd2ztz8/vlwgaU9gO1jo3IKCx7MX4XMAjH1OAcsJlGkkg0idVIHKPNB6oi1h40FeTSV4QrIaRoIhqvh1Q0DhWLCcVTBT3GutYVaMQwwTU614/jFF1IzRL2NzaigYCsaAAeQIRm0QZAMYYAiFcXQMGS1hTI6z4liyk77NHk2OIJaIKSJpn/0YbBjmWseCCWuZ3ecyEki7Pzwrku2jLiAC2Yt2aOMAJHI8JULbiNt0t4CBs1nDRSSPTBoJf8weafbGZ4QzNmYD23xcgYSFHP8kMIOCJmPHSoCGcJsqmMqCgvhiwmUpCk/JXhnjzDny5otIUh1LWJwUswnrkqXesB6YZWHTVQYEJuCmpGgqwjIQa3Wc+ZV1Jfc69rAaZuyLBeNaANQEShHseIWDc6hqYbIiGNHExCWM6riOZSwMvqWSAcCzWCjcqQLe0WISFeZVhwat+zYzRzIw5OlLgKNaq4RC5X74ZTTJgmExSG4mAzLKIyns7c1mPxGe5CzPWtjrQiHFSt2bPYkiXj8UyjfQhhRaMGITeDvhS6GgnuPaH2bjipG5DHgDYhePXPoqdgYXI8tHdIlgF01Yamw/TvgE4FRsh5syTizjw8JPh5ZfFZ6dRGAxcZ4n0tFns+0xRDlUzR3CjmM4wvZfuBkI15AQR3Bp/tLA6aokcyhkEtDQuoHLQoRKUBPZLmJdKfvdWYTzfWgmkOcwG20VgmnPLncVKJKhl+yDpzolDKTlGOMctg0jsksCSThwSSJLdvgi5Ori61wlH8e9zySDRDNMkI7Ce3XTwt38cXW50p1yut3dPvmKlDlZfFhP+k60/7W4X2sZF7vd7eXyoxa1r6PdGDh25hq0e/HTMGHoWLWGjcXVBQ0dnRwczl8fHbQqfL0dzu/PpgfH3571j73XZ9OT02fP9aHVh5c/6s+zaXj952U5X9+9OL+9fv8yfvfh8Pt//rp4+vRsqlKHlzfvN7dvNn/vXLpcv/jh9OLu3Tf1+KdfTt8dL3/f7p6b9IPaXl9ebLY7ml+vz3PThFo3a1mcr2RRZJmkxLJOZZVWZbWspe3Cqp7Lsqs1rmPMZbFq16GGssx5+vDwL/EqTB0='
    

    giaima = decrypt_abe(abe,orig_pk, sk2, ct)
    print(giaima)

# main()