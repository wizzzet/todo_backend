import hashlib


def get_user_auth_token_subject(user):
    salt_hash = hashlib.sha256(user.token_salt.encode('utf-8')).hexdigest()
    return ''.join([x for i, x in enumerate(salt_hash) if i % 4 == 0])
