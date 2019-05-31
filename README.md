# Word Cloud
Visualize Word Frequencies on a web page using Python, Flask and JQCloud

# Flask app server

For db configs see ```app.py``` file

Manual setup

```
$ cd <path of word_cloud>

$ pip install requirements.txt

$ python app.py
```

Docker based setup
```
$ cd <path of word_cloud>

$ docker build -t word_cloud:latest .

$ docker run -it -d -p 5000:5000 word_cloud
```

# MySQL db server

Manual setup
```
$ mysql -u username -p

$ CREATE DATABASE wordscloudapp;

$ USE wordscloudapp;

$ CREATE TABLE `wordscloudapp`.`topwords1` (
  `word_shash` VARCHAR(100) NOT NULL,
  `word` VARCHAR(100) NULL,
  `count` INT(11) UNSIGNED NULL,
  PRIMARY KEY (`word_shash`),
  UNIQUE INDEX `word_shash_UNIQUE` (`word_shash` ASC) VISIBLE);

```

# Best way to safely store and manage the encryption keys
https://security.stackexchange.com/questions/12332/where-to-store-a-server-side-encryption-key

https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/

https://stackoverflow.com/questions/11575398/how-can-i-save-my-secret-keys-and-password-securely-in-my-version-control-system