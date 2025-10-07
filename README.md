# Clause Ease AI

Convert legal contracts to plain English using AI.

Clause Ease AI is an intelligent document processing system that automatically analyzes legal contracts and converts complex legal language into easy-to-understand plain English. The system uses advanced AI models to extract text from documents, detect different types of clauses, identify legal terms, and simplify the language while preserving the original meaning. Perfect for lawyers, businesses, and anyone who needs to quickly understand legal documents without legal expertise.

## Setup

```
# Install
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run
streamlit run webui/streamlit_app.py
```

Open http://localhost:8501 and login with admin / admin123

## What It Does

1. Upload PDF/DOCX/TXT contract
2. Click Process Contract
3. Get simplified text, clause types, and legal terms glossary

## Project Structure

```
src/components/
  module1_document_ingestion.py      # Extract text
  module2_text_preprocessing.py      # Clean text
  module3_clause_detection.py        # Detect clause types
  module4_legal_terms.py             # Extract terms
  module5_language_simplification.py # Simplify text

webui/
  streamlit_app.py                   # Main app
  login.py                           # Authentication

data/
  users.json                         # Login credentials
  sessions.json                      # Logs
```

## Clause Types (15)

Confidentiality, Termination, Indemnity, Dispute Resolution, Governing Law, Payment Terms, IP, Warranties, Liability, Force Majeure, Assignment, Non-Compete, Severability, Amendment, Notice

## AI Models

- BART (facebook/bart-large-cnn) - Simplification
- Legal-BERT - Clause detection
- spaCy - Entity extraction

## Login

Default users in data/users.json:
- admin / admin123
- user / user123

## Speed

- First run: 2-5 min (downloads models)
- CPU: 1-6 min per contract
- GPU: 10-50 sec per contract

## Common Issues

Module not found: pip install -r requirements.txt
Login fails: Check data/users.json exists
PDF error: Remove password or use DOCX/TXT

## Requirements

- Python 3.8+
- 4GB RAM (8GB recommended)
- Internet (first run only)

