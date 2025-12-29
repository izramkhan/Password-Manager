# 🔐 Python Password Manager

A terminal-based password manager written in Python.
This project focuses on **core security concepts**, not UI or convenience.

It was built as a **learning-focused advanced project**, not a production-ready tool.

---

## ❌ What this project does NOT do

* No GUI (command-line only)
* No cloud sync or backups
* No password generation
* No clipboard integration
* No password strength checking for site passwords
* No multi-user support
* Not hardened against advanced attacks
* Not audited or production-grade secure

**Do NOT use this for real sensitive data.**

---

## 🛠 Requirements

* Python 3.9+
* `cryptography` library

Install dependency:

```bash
pip install cryptography
```

---

## ▶️ How to run

1. Clone the repository
2. Run the main file:

```bash
python main.py
```

---

## 📂 Files created by the program

* `master.hash`
  Stores the hashed master password

* `vault.txt`
  Stores encrypted credentials in this format:

  ```
  SITE | USERNAME | ENCRYPTED_PASSWORD
  ```

---

## ⚠️ Security notice

This project is **educational**.

Although real cryptographic primitives are used, the overall system is **not secure enough for real-world usage**.

---

## 👤 Author

**Izram Khan**
