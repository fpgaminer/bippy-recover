This command line script can be used to recover broken Bippy BIP38 keys.

Apparently, Bippy encrypted some Bitcoin private keys incorrectly, making it impossible to decrypt the result in Bippy or other BIP38 applications.

(*At least Bippy versions up to whenever this repo is published*)

This script should allow you to decrypt those keys anyway.  Just do:

    python recover.py BIP38_KEY PASSWORD

You'll need the `scrypt` and `pycrypto` packages installed before running this Python script:

    pip install scrypt
	pip install pycrypto


Donations welcome if this helped you: 1A5EYy78EGP3kgvXUKzHDfi1roonxx2MUo