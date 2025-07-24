#!/usr/bin/env python3
"""
Comprehensive Secure Server Startup for Norshel Web Application
Starts both HTTPS server and HTTP redirect server simultaneously
"""

import os
import sys
import subprocess
import threading
import time
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
        return True
        
    except Exception as e:
        print(f"❌ Error generating SSL certificates: {e}")
        return False

def start_https_server():
    """Start the HTTPS server in a separate thread"""
    try:
        import uvicorn
        print("🔒 Starting HTTPS server on port 8443...")
        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8443,
            reload=True,
            ssl_keyfile="certs/key.pem",
            ssl_certfile="certs/cert.pem",
            log_level="info"
        )
    except Exception as e:
        print(f"❌ HTTPS server error: {e}")

def start_redirect_server():
    """Start the HTTP redirect server in a separate thread"""
    try:
        import uvicorn
        print("🔄 Starting HTTP redirect server on port 8000...")
        # Small delay to let HTTPS server start first
        time.sleep(2)
        uvicorn.run(
            "http_redirect_server:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Redirect server error: {e}")

def main():
    """Main function to start both servers"""
    print("🔐 Norshel Secure Server Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("backend/main.py"):
        print("❌ Error: Please run this script from the project root directory")
        print("   (The directory containing the 'backend' folder)")
        sys.exit(1)
    
    # Generate certificates if needed
    if not generate_ssl_certificates():
        sys.exit(1)
    
    print("\n🚀 Starting Norshel Secure Servers...")
    print("🔒 HTTPS Server: https://localhost:8443")
    print("🔄 HTTP Redirect: http://localhost:8000 → https://localhost:8443")
    print("\n📋 Available secure pages:")
    print("   • https://localhost:8443/ (Home)")
    print("   • https://localhost:8443/login (Parent Login)")
    print("   • https://localhost:8443/dashboard (Dashboard)")
    print("   • https://localhost:8443/programs (Programs)")
    print("   • https://localhost:8443/contact (Contact)")
    print("\n✨ Features:")
    print("   • All HTTP requests automatically redirect to HTTPS")
    print("   • SSL/TLS encryption enabled")
    print("   • Security headers configured")
    print("   • CSRF protection active")
    print("\n⚠️  Browser Security Notice:")
    print("   Since this uses a self-signed certificate, your browser will show")
    print("   a security warning. Click 'Advanced' and 'Proceed to localhost' to continue.")
    print("\n🛑 Press Ctrl+C to stop both servers\n")
    
    try:
        # Start HTTPS server in a separate thread
        https_thread = threading.Thread(target=start_https_server, daemon=True)
        https_thread.start()
        
        # Start HTTP redirect server in main thread (so Ctrl+C works)
        start_redirect_server()
        
    except KeyboardInterrupt:
        print("\n👋 Servers stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 