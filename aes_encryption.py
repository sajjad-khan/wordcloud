from Crypto.Cipher import AES
import base64 # for converting to base64 number
from cryptography.fernet import Fernet

class AESEncryption:
    def __init__(self):
        self._key1 = 'This is a key123' # store somewhere safe
        self._key2 = 'This is an IV456' # store somewhere safe
    
    def encypt(self, message):
        enc_obj = AES.new(self._key1, AES.MODE_CFB, self._key2)
        cipherbytes = enc_obj.encrypt(message)
        b4 = base64.b64encode(cipherbytes)
        final = b4.decode("utf-8")
        return final

    def decrypt(self, ciphertext):
        dec_obj = AES.new(self._key1, AES.MODE_CFB, self._key2)
        string = base64.b64decode(ciphertext)
        dec = dec_obj.decrypt(string)
        return dec.decode("utf-8")

def main():
#    key = Fernet.generate_key() #this is your "password"
#    cipher_suite = Fernet(key)
#    encoded_text = cipher_suite.encrypt(b"Hello stackoverflow!")
#    decoded_text = cipher_suite.decrypt(encoded_text)

    encryptor = AESEncryption()
    sample_word = 'sample word'
    print('orig : ', sample_word)
    # print(type(sample_word))
    encrypted = encryptor.encypt(sample_word)
    decrypted = encryptor.decrypt(encrypted)
    # decrypted = decrypted.decode("utf-8") 
    print('enc : ', encrypted)
    # print(type(encrypted))
    print('dec : ', decrypted)
    # if encrypted == decrypted:
    #     print("same")
    # else:
    #    print("different")

if __name__=='__main__': main()
