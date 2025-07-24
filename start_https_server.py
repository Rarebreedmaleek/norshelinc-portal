#!/usr/bin/env python3
"""
HTTPS Server Startup Script for Norshel Web Application
Generates SSL certificates if needed and starts secure HTTPS server
"""

import os
import sys
from pathlib import Path

def generate_ssl_certificates():
    """Generate self-signed SSL certificates if they don't exist"""
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from datetime import datetime, timedelta
        import ipaddress
    except ImportError:
        print("❌ Error: cryptography package not found. Please install it:")
        print("   pip install cryptography")
        return False
    
    # Create certs directory if it doesn't exist
    os.makedirs("certs", exist_ok=True)
    
    cert_file = "certs/cert.pem"
    key_file = "certs/key.pem"
    
    # Check if certificates already exist
    if os.path.exists(cert_file) and os.path.exists(key_file):
        print("✅ SSL certificates already exist")
        return True
    
    print("🔐 Generating SSL certificates...")
    
    try:
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Create certificate subject
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "State"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "City"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Norshel Inc."),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        # Create certificate
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
                x509.IPAddress(ipaddress.IPv6Address("::1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write private key
        with open(key_file, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Write certificate
        with open(cert_file, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✅ SSL certificates generated successfully!")
        print(f"📁 Certificate: {cert_file}")
        print(f"🔑 Private Key: {key_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error generating SSL certificates: {e}")
        return False

def start_https_server():
    """Start the HTTPS server"""
    try:
        import uvicorn
    except ImportError:
        print("❌ Error: uvicorn not found. Please install it:")
        print("   pip install uvicorn")
        return False
    
    # Generate certificates if needed
    if not generate_ssl_certificates():
        return False
    
    print("\n🚀 Starting Norshel HTTPS Server...")
    print("🔒 HTTPS URL: https://localhost:8443")
    print("🔐 Secure connection enabled")
    print("📋 Available pages:")
    print("   • https://localhost:8443/ (Home)")
    print("   • https://localhost:8443/login (Parent Login)")
    print("   • https://localhost:8443/dashboard (Dashboard)")
    print("   • https://localhost:8443/programs (Programs)")
    print("   • https://localhost:8443/contact (Contact)")
    print("\n⚠️  Browser Security Notice:")
    print("   Since this uses a self-signed certificate, your browser will show")
    print("   a security warning. Click 'Advanced' and 'Proceed to localhost' to continue.")
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    try:
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8443,
            reload=True,
            ssl_keyfile="certs/key.pem",
            ssl_certfile="certs/cert.pem"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🔐 Norshel HTTPS Server Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Error: Please run this script from the project root directory")
        print("   (The directory containing the 'backend' folder)")
        sys.exit(1)
    
    # Start the HTTPS server
    if not start_https_server():
        sys.exit(1) 