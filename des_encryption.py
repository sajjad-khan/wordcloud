from Crypto.Cipher import DES
import base64 # for converting to base64 number

class DESEncryption:
    def __init__(self):
        self._key = '12345678' # store somewhere safe
        self._des = DES.new(self._key, DES.MODE_ECB)
    
    def encypt(self, string):
        text = string
        cipher_text = self._des.encrypt(text)
        return base64.b64encode(cipher_text)

    def decrypt(self, string):
        string = str(base64.b64decode(string), encoding = 'utf_8')
        return self._des.decrypt(string)

def main():
    encryptor = DESEncryption()
    sample_word = 'sample word'
    encrypted = encryptor.encypt(sample_word)
    decrypted = encryptor.decrypt(sample_word)
    print(encrypted)
    if encrypted == decrypted:
        print("same")
    else:
        print("different")


if __name__=='__main__': main()
