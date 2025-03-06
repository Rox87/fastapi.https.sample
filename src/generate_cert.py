from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
import os

def generate_self_signed_cert():
    # Create certificates directory if it doesn't exist
    os.makedirs('certs', exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Create certificate subject and issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost')
    ])
    
    # Certificate validity period
    valid_from = datetime.utcnow()
    valid_to = valid_from + timedelta(days=365)
    
    # Generate certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        valid_from
    ).not_valid_after(
        valid_to
    ).add_extension(
        x509.SubjectAlternativeName([x509.DNSName(u'localhost')]),
        critical=False
    ).sign(private_key, hashes.SHA256())
    
    # Write private key
    with open('certs/key.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write certificate
    with open('certs/cert.pem', 'wb') as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print('Self-signed certificates generated successfully in the certs directory')

if __name__ == '__main__':
    generate_self_signed_cert()