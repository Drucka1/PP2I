
import hashlib


def hash(string):
    hash_object = hashlib.sha256()
    hash_object.update(string.encode())
    return hash_object.hexdigest()

print(len(hash('shsffs1234')))