# This module creates salted hash of a word
# Hashes unlike encryption are one way streat
# You can not get the original word back 

import hashlib, uuid # for salted hash

class SaltedHash:
    def __init__(self):
        # uuid is used to generate a random number to generate salted hash key
        self._salt = uuid.uuid4().hex
        self._sep = ':'
    
    def get_salted_hash(self, word):
        return hashlib.sha256(self._salt.encode() + word.encode()).hexdigest() + self._sep + self._salt
        
    def verify_salted_hash(self, hashed_word, word):
        prev_hash, salt = hashed_word.split(':')
        return prev_hash == hashlib.sha256(salt.encode() + word.encode()).hexdigest()

def main():
    hasher = SaltedHash()
    sample_word = 'sample word'
    shash = hasher.get_salted_hash(sample_word)
    print('word:{}, its s_hash:{}'.format(sample_word, shash))
    if hasher.verify_salted_hash(shash, sample_word):
        print("same")
    else:
        print("different")


if __name__=='__main__': main()
