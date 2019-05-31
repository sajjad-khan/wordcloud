# Word Cloud
Visualize Word Frequencies on a web page using Python, Flask and JQCloud

# Flask app server

Manual setup

For db configs see ```app.py``` file

```
$ cd <path of word_cloud>

$ pip install requirements.txt

$ python app.py
```

Docker setup
```
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
