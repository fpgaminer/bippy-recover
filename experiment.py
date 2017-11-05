import scrypt
from hashlib import sha256
from Crypto.Cipher import AES

#private_key = "CBF4B9F70470856BB4F40F80B87EDB90865997FFEE6DF315AB166D713AF433A5".decode ('hex')
#address = "1Jq6MksXQVWzrznvZzxkV6oY57oWXD9TXB"
#password = "TestingOneTwoThree"
private_key = "e6f634276585c1b25e90fc396ef9793e1ac311dbb4f823c93f94f71d53442dc3".decode ('hex')
#address = "1DBQaqh2axDv4NTTxhAiXPZAtDTzjdp3np" # compressed
address = "12jhTY3xCYz2V4KHr8RrvjDvpocXqcYygo" # uncompressed
password = "testingOneTwo"


def block_xor (a, b):
	result = ""

	for i in xrange (len (a)):
		result += chr (ord (a[i]) ^ ord (b[i]))
	
	return result


salt = sha256 (sha256 (address).digest ()).digest ()[:4]
derived = scrypt.hash (password, salt, N=16384, r=8, p=8, buflen=64)
derivedhalf1 = derived[:32]
derivedhalf2 = derived[32:]

block1 = block_xor (private_key[:16], derivedhalf1[:16])
block2 = block_xor (private_key[16:], derivedhalf1[16:])

encryptedhalf1 = AES.new (derivedhalf2, AES.MODE_ECB).encrypt (block1)
encryptedhalf2 = AES.new (derivedhalf2, AES.MODE_ECB).encrypt (block2)

flagbyte = 0xc0
encrypted_key = "\x01\x42" + chr (flagbyte) + salt + encryptedhalf1 + encryptedhalf2

print "Salt: ", salt.encode ('hex')
print "Encrypted: ", encrypted_key.encode ('hex')