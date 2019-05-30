from flask_mysqldb import MySQL

class DbCtrl:
    def __init__(self, db):
        self._db = db

    def insert_single(self, values):
        # Create cursor
        cur = self._db.connection.cursor()
        # MySQL query string
        query = '''INSERT INTO 
                    topwords(word_shash, word, count) 
                    VALUES(%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    count = VALUES(count)
                    '''
        try:
            result  = cur.execute(query, values)

            # Commit to DB
            self._db.connection.commit()
        except:
            self._db.connection.rollback() 

        # Close connection
        cur.close()

    def insert_many(self, values):
        # Create cursor
        cur = self._db.connection.cursor()
        # MySQL query string
        query = '''INSERT INTO 
                    topwords(word_shash, word, count) 
                    VALUES(%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    count = VALUES(count)
                    '''
        try:
            result  = cur.executemany(query, values)

            # Commit to DB
            self._db.connection.commit()
        except:
            self._db.connection.rollback() 

        # Close connection
        cur.close()

    def list(self):
        # Create curser
        cur = self._db.connection.cursor()

        # Get words
        result = cur.execute("SELECT * FROM topwords ORDER BY count DESC")
        words_list = cur.fetchall()
        cur.close()

        return words_list

def main():
    db = DbCtrl(None)

if __name__=='__main__': main()
