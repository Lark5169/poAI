import hashlib
import json

def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

def hash_object(obj):
    return hash_string(json.dumps(obj, sort_keys=True))