# This module uses wit.ai to do sentiment
# analysis of text on a web page
# ... TODO

from wit import Wit

class WitSentBot:
    def __init__(self):
        access_token = 'some_token'
        self._client = Wit(access_token)

    def do_analysis(self, text):
        # pass
        self._client.message(text)    

def main():
    print("different")


if __name__=='__main__': main()
