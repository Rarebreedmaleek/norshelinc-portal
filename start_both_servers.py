#!/usr/bin/env python3
"""
Start both HTTP and HTTPS servers for Norshel Web Application
HTTP server redirects to HTTPS for security
"""

import os
import sys
import subprocess
import threading
import time

def generate_ssl_certificates():
    """Generate SSL certificates if they don't exist"""
    if os.path.exists("certs/cert.pem") and os.path.exists("certs/key.pem"):
        print("✅ SSL certificates already exist")
        return True
    
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from datetime import datetime, timedelta
        import ipaddress
        
        os.makedirs("certs", exist_ok=True)
        
        # Generate private key
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        
        # Create certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Norshel Inc."),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
            private_key.public_key()
        ).serial_number(x509.random_serial_number()).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("127.0.0.1"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).sign(private_key, hashes.SHA256())
        
        # Write files
        with open("certs/key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open("certs/cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✅ SSL certificates generated!")
        return True
    except Exception as e:
        print(f"❌ Error generating certificates: {e}")
        return False

def start_https_server():
    """Start HTTPS server"""
    os.system('venv\\Scripts\\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8443 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem --reload')

def start_http_server():
    """Start HTTP server (with redirect to HTTPS)"""
    time.sleep(2)  # Let HTTPS server start first
    os.system('venv\\Scripts\\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload')

def main():
    print("🔐 Starting Norshel Secure Servers")
    print("=" * 40)
    
    if not os.path.exists("backend/main.py"):
        print("❌ Error: Run from project root directory")
        sys.exit(1)
    
    if not generate_ssl_certificates():
        sys.exit(1)
    
    print("\n🚀 Starting servers...")
    print("🔒 HTTPS: https://localhost:8443")
    print("🔄 HTTP: http://localhost:8000 (redirects to HTTPS)")
    print("\n🛑 Press Ctrl+C to stop\n")
    
    try:
        # Start HTTPS server in background thread
        https_thread = threading.Thread(target=start_https_server, daemon=True)
        https_thread.start()
        
        # Start HTTP server in main thread
        start_http_server()
    except KeyboardInterrupt:
        print("\n👋 Servers stopped")

if __name__ == "__main__":
    main() 