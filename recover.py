import scrypt
import sys
from hashlib import sha256
from Crypto.Cipher import AES
from base58 import *

def block_xor (a, b):
	result = ""

	for i in xrange (len (a)):
		result += chr (ord (a[i]) ^ ord (b[i]))
	
	return result


# Grab command line arguments
if len (sys.argv) != 3:
	print "USAGE: ", sys.argv[0], "BIP38_KEY PASSWORD"
	sys.exit (-1)

bip38_key = sys.argv[1]
password = sys.argv[2]

# Try decoding the key as Base58Check
decoded_bip38_key = b58decode_check (bip38_key)

# Do some checks and break apart into its various pieces
if decoded_bip38_key[:2] != '\x01\x42':
	print "WARNING: This probably isn't a BIP38 encoded key, but we're going to try anyway"

flagbits = decoded_bip38_key[2]
checksum = decoded_bip38_key[3:7]
encrypteddata = decoded_bip38_key[7:]

if len (encrypteddata) != 32:
	print "ERROR: This definitely isn't a BIP38 encoded key.  It's too short."
	sys.exit (-1)

# Okay, let's start decrypting
derived = scrypt.hash (password, checksum, N=16384, r=8, p=8, buflen=64)
derivedhalf1 = derived[:32]
derivedhalf2 = derived[32:]

decryptedhalf1 = AES.new (derivedhalf2, AES.MODE_ECB).decrypt (encrypteddata[:16])
decryptedhalf2 = AES.new (derivedhalf2, AES.MODE_ECB).decrypt (encrypteddata[16:])

block1 = block_xor (decryptedhalf1, derivedhalf1[:16])
block2 = block_xor (decryptedhalf2, derivedhalf1[16:])

private_key = block1 + block2

wif1 = "\x80" + private_key
wif2 = "\x80" + private_key + "\x01"

print "These are the two possible original private keys.  Just import both."
print b58encode_check (wif1)
print b58encode_check (wif2)