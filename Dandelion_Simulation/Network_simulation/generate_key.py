import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

def generate_keys():
    # Generate private key for ECC
    private_key = ec.generate_private_key(
        ec.SECP256R1(),  # Using the SECP256R1 curve
        backend=default_backend()
    )
    
    # Serialize private key to PEM format
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8').replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "").strip()

    # Generate public key
    public_key = private_key.public_key()
    
    # Serialize public key to PEM format
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8').replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").strip()

    return pem_private, pem_public

# Read the peer IDs from the file
with open("peerids.txt", "r") as file:
    peer_ids = [line.strip() for line in file]

# Prepare a dictionary to store peer IDs and their keys
peerid_key_dict = {}
public_key_dict = {}

for peer_id in peer_ids:
    private_key, public_key = generate_keys()
    peerid_key_dict[peer_id] = {"private_key": private_key, "public_key": public_key}
    public_key_dict[peer_id] = public_key

# Write the dictionary to the file in the desired format
with open("peerids_keys.txt", "w+") as file:
    file.write(str(peerid_key_dict))

# Write the public keys to the public_key_list.txt file in dictionary format
with open("public_key_list.txt", "w+") as file:
    file.write(str(public_key_dict))
