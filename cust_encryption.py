# This module has base64 custom encryption 
# for performance purposes

import base64 # for converting to base64 number

class CustEncryption:
    def __init__(self):
        self._key = '1234567890123456' # store somewhere safe
    
    def encypt(self, string):
        encoded_chars = []
        for i in range(len(string)):
            key_c = self._key[i % len(self._key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return base64.b64encode(bytes(encoded_string, "utf-8"))

    def decrypt(self, string):
        string = str(base64.b64decode(string), encoding = 'utf_8')
        encoded_chars = []
        for i in range(len(string)):
            key_c = self._key[i % len(self._key)]
            encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = ''.join(encoded_chars)
        return encoded_string

def main():
    encryptor = CustEncryption()
    sample_word = 'sample word'
    encrypted = encryptor.encypt(sample_word)
    decrypted = encryptor.decrypt(sample_word)
    print(encrypted)
    if encrypted == decrypted:
        print("same")
    else:
        print("different")


if __name__=='__main__': main()
