import hash
import password.password_guess as password_guess


password = input("Give me a password to try to reconstruct (lowercase letters only): ")
pass_hash = hash.simple_hash(password)
print("Password: {:s} (hash {:d})".format(password, pass_hash))

guessed_pass = password_guess.guess_password(hash.simple_hash(password), 10, len(password), hash.simple_hash)
guess_hash = hash.simple_hash(guessed_pass)
print("Guessed Password: {:s} (hash {:d})".format(guessed_pass, guess_hash))
diff = abs(guess_hash-pass_hash)
print("Absolute difference between hashes: {:d} ({:.5f}% error)".format(diff, diff/pass_hash*100))
