# ClauseEase AI - Contract Language Simplifier

> **An AI-powered Flask web application that simplifies complex legal contract language into easy-to-understand plain text.**

Automatically detect clauses, extract legal terms, and transform complicated contracts into readable summaries - all with the power of Natural Language Processing and AI.

---

## 🚀 Features

✅ **AI-Powered Clause Detection** - Automatically identifies and categorizes contract clauses  
✅ **Multi-Format Document Support** - Upload PDF, DOCX, or TXT files  
✅ **Smart Language Simplification** - Converts legal jargon into plain, simple language  
✅ **Legal Term Glossary** - Explains complex legal terms in simple words  
✅ **Interactive Results Dashboard** - Compare original vs simplified text side-by-side  
✅ **Readability Metrics** - Analyze text complexity with scores and charts  
✅ **Document History** - Save and revisit previously processed contracts  
✅ **User Authentication** - Secure login and registration system  

---

## 📋 Prerequisites

Before running this project, ensure you have:

- **Python 3.8 or higher** installed ([Download Python](https://www.python.org/downloads/))
- **pip** package manager (comes with Python)
- **Git** (for cloning the repository)
- **At least 2GB RAM** (for NLP model processing)
- **Internet connection** (for downloading NLP models on first run)

---

## 🛠️ Installation & Setup

Follow these steps **carefully** to run the project on your local machine:

### **Step 1: Clone the Repository**

Open your terminal (Command Prompt/PowerShell on Windows, Terminal on Mac/Linux) and run:

```bash
git clone https://github.com/Sourabsb/Clause_Ease_AI_Based_Contract_Language_Simplifier.git
cd Clause_Ease_AI_Based_Contract_Language_Simplifier
```

---

### **Step 2: Create a Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ **You should see `(venv)` prefix in your terminal** indicating the virtual environment is active.

---

### **Step 3: Install Python Dependencies**

Make sure your virtual environment is activated, then run:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

⏳ This will take **2-5 minutes** depending on your internet speed.

---

### **Step 4: Download Required NLP Models**

The application uses spaCy and NLTK for Natural Language Processing. Download the required models:

**For NLTK:**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')"
```

**For spaCy:**
```bash
python -m spacy download en_core_web_sm
```

⏳ This step may take **3-5 minutes**.

---

### **Step 5: Set Up Environment Variables (Optional)**

For production deployments, it's recommended to set a custom secret key:

1. Copy the example environment file:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**
```bash
cp .env.example .env
```

2. Edit the `.env` file and set your own `SECRET_KEY`:

```
SECRET_KEY=your-random-secret-key-here
```

🔒 For development, this step is **optional** (a default key will be used).

---

### **Step 6: Run the Flask Application**

Now you're ready to start the server! Run:

```bash
python src/app.py
```

✅ **The application will start on:** `http://localhost:5000`

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

🌐 **Open your browser and go to:** [http://localhost:5000](http://localhost:5000)

---

## 🎯 How to Use the Application

### **1️⃣ Register a New Account**
- Navigate to **http://localhost:5000/auth/login**
- Click on **"Create Account"** or go to **http://localhost:5000/auth/register**
- Fill in your username, email, and password
- Click **"Sign Up"**

### **2️⃣ Login**
- Enter your registered email and password
- Click **"Sign In"**

### **3️⃣ Upload a Contract Document**
- On the dashboard, click **"Upload Contract"** button
- Select a contract file (PDF, DOCX, or TXT format)
- Click **"Submit"** and wait for processing (30-60 seconds)

### **4️⃣ View Results**
The results page shows:
- **Original Text** vs **Simplified Text** comparison
- **Detected Clauses** with types (e.g., Payment, Confidentiality, Termination)
- **Legal Terms** with simple explanations
- **Readability Metrics** and charts
- **Statistics Comparison** (word count, sentence count, etc.)

### **5️⃣ Download Report**
- Click **"Download Report"** button to export results as JSON file

### **6️⃣ View Document History**
- Click **"Document History"** to see all previously processed contracts
- Click on any document to view its results again

---

## 📂 Project Structure

```
Clause_Ease_AI_Based_Contract_Language_Simplifier/
│
├── src/                                # Main application code
│   ├── app.py                          # Flask application entry point
│   └── components/                     # Core NLP processing modules
│       ├── module1_document_ingestion.py       # PDF/DOCX/TXT extraction
│       ├── module2_text_preprocessing.py       # Text cleaning
│       ├── module3_clause_detection.py         # Clause classification
│       ├── module4_legal_terms.py              # Legal term extraction
│       ├── module5_language_simplification.py  # Text simplification
│       └── readability_metrics.py              # Readability scoring
│
├── templates/                          # HTML templates (Jinja2)
│   ├── base.html                       # Base layout
│   ├── login.html                      # Login page
│   ├── register.html                   # Registration page
│   ├── landing.html                    # Main dashboard
│   ├── results.html                    # Results display page
│   └── history.html                    # Document history page
│
├── static/                             # CSS and JavaScript files
│   ├── css/                            # Stylesheets
│   │   ├── auth.css                    # Login/Register styling
│   │   ├── landing.css                 # Dashboard styling
│   │   ├── results.css                 # Results page styling
│   │   └── history.css                 # History page styling
│   └── js/                             # JavaScript files
│       ├── landing.js                  # Dashboard functionality
│       └── results.js                  # Results page functionality
│
├── scripts/                            # Utility scripts
│   ├── download_models.py              # NLP model downloader
│
├── data/                               # Database storage (auto-created)
│   └── clauseease.db                   # SQLite database
│
├── temp_uploads/                       # Temporary file storage (auto-created)
│
├── requirements.txt                    # Python dependencies
├── .env.example                        # Environment variables template
├── .gitignore                          # Git ignore rules
└── README.md                           # This file
```

---

## 🔧 Troubleshooting Common Issues

### ❌ **Issue: Port 5000 already in use**

**Solution (Windows PowerShell):**
```powershell
$process = Get-NetTCPConnection -LocalPort 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($process) { Stop-Process -Id $process -Force }
```

**Solution (macOS/Linux):**
```bash
lsof -ti:5000 | xargs kill -9
```

Then restart the Flask app: `python src/app.py`

---

### ❌ **Issue: spaCy model not found**

**Error:** `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

---

### ❌ **Issue: ModuleNotFoundError**

**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:** Make sure your virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

---

### ❌ **Issue: Database locked error**

**Solution:** Stop all running Flask instances and delete the database file:

**Windows:**
```powershell
Remove-Item data\clauseease.db -Force
```

**macOS/Linux:**
```bash
rm data/clauseease.db
```

Then restart the application - a fresh database will be created automatically.

---

## 📦 Dependencies

This project uses the following key Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| SQLAlchemy | 2.0.36 | Database ORM |
| Flask-Login | 0.6.3 | User authentication |
| spaCy | 3.7.2 | NLP processing |
| transformers | 4.56.2 | AI language models |
| PyTorch | 2.8.0 | Deep learning backend |
| NLTK | 3.8.1 | Text tokenization |
| PyMuPDF | 1.23.8 | PDF text extraction |
| python-docx | 1.1.0 | DOCX text extraction |
| matplotlib | 3.8.2 | Chart generation |
| seaborn | 0.13.0 | Statistical visualization |

See `requirements.txt` for the complete list.

---

## 🛡️ Security Recommendations

- ✅ Change the `SECRET_KEY` in `.env` file for production deployments
- ✅ Use strong, unique passwords for user accounts
- ✅ Keep dependencies updated regularly: `pip install --upgrade -r requirements.txt`
- ✅ **Never commit** `.env` files or sensitive data to version control
- ✅ Use HTTPS in production environments

---

## 📄 License

This project is developed for **educational and research purposes**.

---

## 👨‍💻 Author

**Sourab Singh**  
🔗 GitHub: [@Sourabsb](https://github.com/Sourabsb)  
📦 Repository: [Clause_Ease_AI_Based_Contract_Language_Simplifier](https://github.com/Sourabsb/Clause_Ease_AI_Based_Contract_Language_Simplifier)

---

## 🙏 Acknowledgments

- 🤗 **Hugging Face** - For transformer models and NLP tools
- 🏢 **spaCy** - For powerful NLP capabilities
- 🌐 **Flask** - For excellent web framework documentation
- 💡 **Open Source Community** - For continuous innovation

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

**Made with ❤️ for simplifying legal language**
