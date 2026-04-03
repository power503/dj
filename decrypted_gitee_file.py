# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 10:10:22 2026

@author: ...
"""

# pip install pycryptodome


from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests



def aes_ecb_decrypt(ciphertext_b64: str, key: str) -> str:
    """
    使用 AES ECB 模式解密字符串。

    :param ciphertext_b64: Base64 编码的密文字符串。
    :param key: 密钥字符串，必须与加密时使用的密钥相同。
    :return: 解密后的明文字符串。
    """
    # 将字符串密钥和 Base64 密文转换回字节
    key_bytes = key.encode('utf-8')
    ciphertext_bytes = base64.b64decode(ciphertext_b64)

    # 创建 AES cipher 对象，指定 ECB 模式
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    # 执行解密
    padded_plaintext_bytes = cipher.decrypt(ciphertext_bytes)
    
    # 去除 PKCS7 填充
    plaintext_bytes = unpad(padded_plaintext_bytes, AES.block_size)
    
    return plaintext_bytes.decode('utf-8')

def get_content(url,save_name):
    
    # 16字节的密钥，对应 AES-128
    my_key = "cb745bb440731e3e" # 自用数据，key可公开，在gitee上进行aes加密数据只是为了不被和谐掉，个人得到这个key也没啥用处。。。
    my_encrypted_data = requests.get(url).text

    # print(f"原始数据: {my_encrypted_data}")
    # print(f"密钥: {my_key}")

    # # 加密
    # encrypted_data = aes_ecb_encrypt(my_data, my_key)
    # print(f"加密后 (Base64): {encrypted_data}")
    
    

    # 解密
    decrypted_data = aes_ecb_decrypt(my_encrypted_data, my_key)
    # print(f"解密后: {decrypted_data}")
    
    with open(save_name, 'w', encoding='utf-8') as f:
        f.write(decrypted_data)
        print(f"已写入文件:{save_name}")
if __name__ == "__main__":
    
    
    u1 = 'https://gitee.com/isforker/iptv/raw/master/live_git.txt'
    u2 = 'https://gitee.com/isforker/iptv/raw/master/live.txt'
    
    get_content(u1, 'live_github.txt')
    get_content(u2, 'live_giteee.txt')
    
