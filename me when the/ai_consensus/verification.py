import hashlib

def verify_ai_proof(block_header, ai_proof, difficulty):
    test_hash = hashlib.sha256(
        block_header + str(ai_proof['nonce']).encode()
    ).hexdigest()
    return (
        test_hash == ai_proof['hash'] and
        test_hash.startswith('0'*difficulty)
    )