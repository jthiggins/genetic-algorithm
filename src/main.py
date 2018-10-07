import hash
import password.password_guess as password_guess


# Comment these lines out if you want to uncomment the lines below
password = input("Give me a password to try to reconstruct (letters and numbers only): ")
length = len(password)
pass_hash = hash.simple_hash(password)
print("Password: {:s} (hash {:d})".format(password, pass_hash))

# Uncomment the lines in password_guess.py if you want to uncomment these lines
#pass_hash = int(input("Give me a hash! "))
#length = int(input("Give me a length! "))

guessed_pass = password_guess.guess_password(pass_hash, length, hash.simple_hash)

guess_hash = hash.simple_hash(guessed_pass)
print("Reconstructed Password: {:s} (hash {:d})".format(guessed_pass, guess_hash))
diff = abs(guess_hash-pass_hash)
g = hash.simple_hash(guessed_pass)
print("Absolute difference between hashes: {:d} ({:.5f}% error)".format(diff, diff/pass_hash*100))
