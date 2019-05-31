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
1) Use an external Hardware Security Module. There is an entire industry of products designed for offloading security-sensitive operations to external devices. This doesn't solve the problem so much as relocate it, but it relocates it to device that is far more secure, so altogether it's a security win. If you're doing anything high-stakes, then this is almost certainly going to factor into your solution.

2) Tie the encryption key to your hardware. TPM chips are useful for this, as are USB security tokens (not flash drives, though). In this case, crypto only works on that specific piece of hardware, but isn't otherwise restricted. It's a bit like the kid-sidekick version of the HSM mentioned above. Google's recently-announced Project Vault takes this a step further by making a high-bandwidth HSM embeddable into even the smallest consumer devices.

https://security.stackexchange.com/questions/12332/where-to-store-a-server-side-encryption-key

https://en.wikipedia.org/wiki/Hardware_security_module

https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/

https://stackoverflow.com/questions/11575398/how-can-i-save-my-secret-keys-and-password-securely-in-my-version-control-system