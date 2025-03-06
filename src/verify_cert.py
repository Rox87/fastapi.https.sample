from cryptography import x509
from cryptography.hazmat.primitives import serialization

with open('certs/cert.pem', 'rb') as f:
    cert = x509.load_pem_x509_certificate(f.read())
    print(f'Valid until: {cert.not_valid_after}')
    print(f'Subject: {cert.subject.rfc4514_string()}')