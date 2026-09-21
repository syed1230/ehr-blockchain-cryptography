# 🔐 EHR Blockchain Security System

A cryptographic security model for protecting Electronic Health Records (EHR) using AES-256 encryption, SHA-256 hashing, and blockchain technology.

## 🎯 Objective

The project demonstrates how cryptographic techniques can be used to protect sensitive healthcare records and detect unauthorized modification.

## 🔄 System Workflow

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

## 🔐 Technologies Used

- Python
- Streamlit
- AES-256-GCM
- SHA-256
- Blockchain
- Cryptography Library

## ✨ Features

- Secure patient record entry
- AES-256 encryption
- SHA-256 hashing
- Blockchain-based record storage
- Blockchain integrity verification
- Tampering simulation
- Tamper detection
- Authorized patient record decryption
- Interactive Streamlit dashboard

## 🏥 Patient Data

The system allows users to enter:

- Patient Name
- Patient ID
- Age
- Blood Group
- Diagnosis

The patient record is encrypted before being stored in the blockchain.

## 🛡️ Security Demonstration

The application allows intentional modification of a blockchain block.

After modification, blockchain verification detects the change and reports:

"TAMPER DETECTED!"

This demonstrates how hash-based blockchain linking can help identify unauthorized data modification.

## 📂 Project Structure

ehr-blockchain-cryptography/
│
├── app.py
├── crypto_utils.py
├── blockchain.py
└── README.md

## 🚀 How to Run

Install the required libraries:

```bash
pip install streamlit cryptography
