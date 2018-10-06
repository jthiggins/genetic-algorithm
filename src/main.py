import hash
import password.password_crack as password_crack


password = "ants"
print("{:s} = {:d}".format(password, hash.simple_hash(password)))
print("Password:", password)

guessed_pass = password_crack.attempt_crack(hash.simple_hash(password), 1000, 4, hash.simple_hash)
print("Guessed Password:", guessed_pass)
print("{:s} = {:d}".format(guessed_pass, hash.simple_hash(guessed_pass)))
