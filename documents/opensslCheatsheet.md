# 🔐 OpenSSL CLI Cheatsheet
> This guide explains not just *how* to use OpenSSL commands, but also *why* you use them. Includes commands for working with keys, CSRs, certificates, conversions, and validations.
---
## 📚 Table of Contents
- [🔑 Generate Private Keys](#-generate-private-keys)
- [📄 Create Certificate Signing Request (CSR)](#-create-certificate-signing-request-csr)
- [🔏 Generate Self-Signed Certificates](#-generate-self-signed-certificates)
- [🔍 Inspect Certificates, CSRs, Keys](#-inspect-certificates-csrs-keys)
- [🔁 Convert Certificate Formats](#-convert-certificate-formats)
- [📦 Create .PFX/.P12 Bundles](#-create-pfxp12-bundles)
- [🔐 Add or Remove Key Passphrase](#-add-or-remove-key-passphrase)
- [🧪 Verify Certificates](#-verify-certificates)
- [🌐 Check Remote SSL Connection](#-check-remote-ssl-connection)
- [🧰 Miscellaneous Utilities](#-miscellaneous-utilities)
- [📁 Common File Extensions](#-common-file-extensions)
---
## 🔑 Generate Private Keys
```bash
# Generate a new 2048-bit RSA private key
openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048
```
> ✅ Why? You need a private key to initiate certificate creation or for secure communication.
```bash
# Legacy method (still common)
openssl genrsa -out private.key 2048
```
> ✅ Why? This is used for backwards compatibility or where genpkey is not available.
---
## 📄 Create Certificate Signing Request (CSR)
```bash
openssl req -new -key private.key -out request.csr
```
> ✅ Why? You generate a CSR to request an SSL certificate from a Certificate Authority (CA). It includes your public key and identity details.
Automated:
```bash
openssl req -new -key private.key -out request.csr \
  -subj "/C=CA/ST=Quebec/L=Montreal/O=YourOrg/OU=Dev/CN=example.com"
```
> ✅ Why? Automation helps in CI/CD or scripting environments.
---
## 🔏 Generate Self-Signed Certificates
```bash
openssl req -x509 -new -nodes -key private.key -sha256 -days 365 -out cert.pem
```
> ✅ Why? Useful for internal testing or development where a trusted CA is not required.
---
## 🔍 Inspect Certificates, CSRs, Keys
```bash
openssl x509 -in cert.pem -text -noout
```
> ✅ Why? See validity, issuer, subject, SANs, etc.
```bash
openssl req -in request.csr -noout -text
```
> ✅ Why? Validate CSR contents before submission.
```bash
openssl rsa -in private.key -check
```
> ✅ Why? Verify key integrity and view modulus.
---
## 🔁 Convert Certificate Formats
```bash
openssl x509 -in cert.pem -outform der -out cert.der
```
> ✅ Why? Convert PEM (text) to DER (binary) for Windows/Java apps.
```bash
openssl pkcs8 -topk8 -in private.key -out key.pk8 -nocrypt
```
> ✅ Why? Required by systems like Kubernetes secrets or Java keystores.
---
## 📦 Create .PFX/.P12 Bundles
```bash
openssl pkcs12 -export -out cert.pfx -inkey private.key -in cert.pem -certfile ca-bundle.pem
```
> ✅ Why? Bundle certificate and key for import into Windows, browsers, Java, etc.
---
## 🔐 Add or Remove Key Passphrase
```bash
openssl rsa -aes256 -in private.key -out private_encrypted.key
```
> ✅ Why? Protect private keys with a passphrase for added security.
```bash
openssl rsa -in private_encrypted.key -out private.key
```
> ✅ Why? Remove passphrase for automation tools like web servers.
---
## 🧪 Verify Certificates
```bash
openssl x509 -noout -modulus -in cert.pem | openssl md5
openssl rsa -noout -modulus -in private.key | openssl md5
```
> ✅ Why? Ensure the cert and private key match (modulus must be identical).
```bash
openssl verify -CAfile ca_bundle.pem cert.pem
```
> ✅ Why? Check if the cert chains back to a valid root/intermediate CA.
---
## 🌐 Check Remote SSL Connection
```bash
openssl s_client -connect google.com:443
```
> ✅ Why? Debug cert chain, cipher, and TLS version used by live server.
```bash
openssl s_client -connect example.com:443 -servername example.com
```
> ✅ Why? Test SNI (Server Name Indication) which is required for multi-host setups.
---
## 🧰 Miscellaneous Utilities
```bash
openssl base64 -d -in encoded.pem -out decoded.bin
```
> ✅ Why? Decode PEM or secret from base64 format.
```bash
openssl rand -hex 16
```
> ✅ Why? Generate 16-byte (128-bit) secure random token, useful for API keys.
---
## 📁 Common File Extensions
| Extension | Description                      | Use Case                       |
|-----------|----------------------------------|--------------------------------|
| `.key`    | Private Key                      | Required for SSL setup         |
| `.csr`    | Certificate Signing Request      | Sent to CA                     |
| `.crt` / `.pem` | Public Certificate         | Used by servers and clients    |
| `.pfx` / `.p12` | Cert + Key Bundle (binary) | Import into Windows/Java/etc   |
| `.der`    | Binary Certificate               | Used in Windows/Java apps      |
---
