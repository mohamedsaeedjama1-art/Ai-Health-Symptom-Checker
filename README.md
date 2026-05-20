# 🏥  AI Health Symptom Checker

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![Ollama](https://img.shields.io/badge/Ollama-0.19.0-orange.svg)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

**AI Health Symptom Checker** is an intelligent web application that analyzes user symptoms using artificial intelligence and provides health insights. Built with Flask and powered by Ollama's llama3.2:1b model.



### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Powered Analysis** | Uses Ollama llama3.2:1b to analyze symptoms |
| 🔐 **User Authentication** | Secure Sign Up / Sign In with session management |
| 📜 **Chat History** | LocalStorage-based history (browser storage) |
| 🌍 **Language Validation** | English-only input detection (Somali filter) |
| ❌ **Non-Health Filtering** | Blocks unrelated questions automatically |
| 🎨 **Modern UI** | Dark theme with responsive sidebar |
| 💾 **Session Management** | Server-side session storage (Flask-Session) |

---

## 👥 Project Team

| # | Name 
|---|------
| 1 | **Mohammad Sa'ed Jama** 
| 2 | **Abdirahim Garaad Mohammad**  
| 3 | **Abdilahi Ali Jamac** 
| 4 | **Abdirahman Abdirisack Osman** 
| 5 | **Sakariye Sidik Elmi** 
| 6 | **Liibaan Muhumed Jaamac**  
| 7 | **Abdiqani Mohammad Ali** 
| 8 | **Sakariye Mohammad Cawale**  
| 9 | **Abdishakur Osman Farah** 

---

## 🛠️ Technology Stack & Tools

### Backend Tools
| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.13+ | Core programming language |
| **Flask** | 3.0.3 | Web framework |
| **Flask-Session** | 0.8.0 | Server-side session management |
| **Flask-CORS** | 4.0.0 | Cross-origin resource sharing |
| **Requests** | 2.33.1 | HTTP requests to Ollama API |

### AI Engine
| Tool | Version | Purpose |
|------|---------|---------|
| **Ollama** | 0.19.0+ | Local AI model runner |
| **Llama3.2:1b** | Latest | Lightweight LLM for symptom analysis |

### Frontend Tools
| Tool | Purpose |
|------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling & animations |
| **JavaScript** | Interactivity & API calls |
| **Google Fonts** | Syne & DM Sans typography |

### Storage System
| Type | Location | Purpose |
|------|----------|---------|
| **LocalStorage** | Browser (Client-side) | User history storage |
| **Flask-Session** | `flask_session/` folder | Temporary session data |

> **Note:** We use **LocalStorage** (browser storage) for chat history. Each user's history is stored in their own browser.

### Development Tools
| Tool | Purpose |
|------|---------|
| **VS Code** | Code editor |
| **Git** | Version control |
| **GitHub** | Repository hosting |
| **PowerShell** | Terminal / Command line |
| **Chrome DevTools** | Debugging & testing |

---


## How To Run 

1. Go to  **Terminal**
2. Then Write **python app.py**
3. Then Copy The Url **http://127.0.0.1:0000/**  -- *Example*
4. Finally Paste and Run To Your Browsers Like **Chrome, Firefox, Microsft Edge ..**

---


## 📦 Packages Installed

```txt
Flask==3.0.3
Flask-CORS==4.0.0
Flask-Session==0.8.0
requests==2.33.1