# 🔐 EHR Blockchain Security System

A cryptographic security model for protecting **Electronic Health Records (EHR)** using AES-256 encryption, SHA-256 hashing, and blockchain technology.

## 🎯 Objective

The project demonstrates how cryptographic techniques can be used to protect sensitive healthcare records and detect unauthorized modification.

## 🔄 System Workflow
```text 
Patient Record
      ↓
AES-256 Encryption
      ↓
SHA-256 Hashing
      ↓
Blockchain Storage
      ↓
Integrity Verification
      ↓
Tamper Detection
      ↓
Authorized Decryption
```
## 🔐 Technologies Used

- Python
- Streamlit
- AES-256-GCM
- SHA-256
- PBKDF2-SHA256
- Blockchain
- Cryptography Library
- CSV Storage
```
```
## ✨ Features

- Secure patient record entry
- User authentication
- Admin and Doctor roles
- Unique Patient ID validation
- AES-256-GCM encryption
- SHA-256 hashing
- Blockchain-based record storage
- Blockchain integrity verification
- Automatic tamper detection
- Authorized patient record decryption
- Persistent CSV storage
- Interactive Streamlit dashboard

## 🏥 Patient Data

The system allows authorized users to enter:

- Patient ID
- Patient Name
- Age
- Gender
- Blood Group
- Diagnosis

The patient record is encrypted using AES-256-GCM before being stored in the blockchain.

## 👤 Authentication

The system provides authentication for authorized users.

Available roles:

- Admin
- Doctor

Passwords are verified using PBKDF2 with SHA-256.

## 🆔 Unique Patient ID

Each patient must have a unique Patient ID.

The system checks existing records before storing a new patient record. If the Patient ID already exists, the system prevents duplicate entry.

## ⛓️ Blockchain Structure

Each patient record is stored in a blockchain block.

Each block contains:

- Block Index
- Timestamp
- Encrypted Patient Data
- SHA-256 Data Hash
- Previous Block Hash
- Current Block Hash

The blocks are connected using the previous block hash.

```text
Genesis Block
      ↓
   Block 1
      ↓
   Block 2
      ↓
   Block 3
```
## 🛡️ Integrity Verification

The system automatically verifies the integrity of the blockchain.

It checks:

1. The SHA-256 hash of the encrypted data.
2. The current block hash.
3. The previous block hash connection.

If the stored data or blockchain information is modified, the verification can detect the inconsistency.

The system displays:

```text
🚨 TAMPER DETECTED!
Blockchain integrity has been compromised.
```

## 🔓 Authorized Decryption

After authentication and integrity verification, authorized users can decrypt patient records.

```text
Encrypted Patient Data
        ↓
Integrity Verification
        ↓
AES-256-GCM Decryption
        ↓
Original Patient Record
```

## 💾 Persistent Storage

Patient blockchain records are stored in a CSV file.

Stored information includes:

- Patient ID
- Encrypted Data
- Data Hash
- Block Hash
- Previous Hash
- Timestamp

The AES encryption key is stored separately and excluded from Git using `.gitignore`.

> CSV storage is used for educational purposes and is not intended for production healthcare data.

## 📂 Project Structure

```text
ehr-blockchain-cryptography/
│
├── app.py
├── blockchain.py
├── crypto_utils.py
├── storage.py
├── auth.py
├── README.md
└── .gitignore
```

## 🚀 How to Run

Install the required libraries:

```bash
pip install streamlit cryptography
```
Run the application:

```bash
streamlit run app.py
```
## ⚠️ Project Scope

This project demonstrates the use of **cryptography and blockchain concepts** to secure Electronic Health Records (EHRs).

It focuses on:

- Encryption
- Hashing
- Blockchain hash chaining
- Integrity verification
- Authentication
- Authorized access
- Tamper detection

> This project is developed for **academic demonstration purposes** and is not intended for production healthcare use.
