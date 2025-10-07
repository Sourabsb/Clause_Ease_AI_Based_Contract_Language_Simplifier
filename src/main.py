from components.module1_document_ingestion import extract_text
from components.module2_text_preprocessing import preprocess_contract_text
import os
import json

# Optional advanced modules (they have safe fallbacks if heavy libs not installed)
from components.module3_clause_detection import detect_clause_type, ensure_model_loaded
from components.module5_language_simplification import simplify_text, ensure_simplifier_loaded
from components.module4_legal_terms import extract_legal_terms

def run_main_app(username):
    """Main application function that runs after successful login"""
    print(f"\n{'='*80}")
    print(f"CLAUSE EASE AI - CONTRACT LANGUAGE SIMPLIFIER")
    print(f"Welcome, {username}!")
    print(f"{'='*80}")

    # Step 1: Extract text from contract file
    contract_file = "Contract document.pdf"

    if not os.path.exists(contract_file):
        print(f"Error: Contract file '{contract_file}' not found!")
        return

    print(f"\nProcessing contract file: {contract_file}")
    raw_text = extract_text(contract_file)

    if not raw_text.startswith("[ERROR]"):
        print("✓ Document extraction successful!")

        # Step 2: Preprocess the extracted text
        processed_clauses = preprocess_contract_text(raw_text)

        print(f"✓ Text preprocessing completed!")
        print(f"✓ Total clauses found: {len(processed_clauses)}")

        # Save session info
        save_session_info(username, len(processed_clauses))

        # Display complete processed text
        print(f"\n{'='*80}")
        print("COMPLETE PROCESSED CONTRACT TEXT")
        print(f"{'='*80}")

        # Try to lazily load heavy models only if available in the environment
        # These calls will return False if transformers/torch are not installed
        ensure_model_loaded()
        ensure_simplifier_loaded()

        for i, clause in enumerate(processed_clauses, 1):
            print(f"\n--- CLAUSE {i} ---")
            print(f"Raw Text: {clause['raw_text']}")
            print(f"Cleaned Text: {clause['cleaned_text']}")
            print(f"\nSentences ({len(clause['sentences'])}):")
            for j, sentence in enumerate(clause['sentences'], 1):
                print(f"  {j}. {sentence}")

            if clause['entities']:
                print(f"\nEntities ({len(clause['entities'])}):")
                for entity, label in clause['entities']:
                    print(f"  - {entity} ({label})")
            else:
                print("\nEntities: None found")

            # Advanced: detect clause type, extract legal terms, and simplify clause
            clause_type = detect_clause_type(clause['cleaned_text'])
            print(f"\nDetected Clause Type: {clause_type}")

            terms = extract_legal_terms(clause['cleaned_text'])
            if terms:
                print(f"\nLegal Terms ({len(terms)}):")
                for t, norm in terms:
                    print(f"  - {t} -> {norm}")

            simplified = simplify_text(clause['cleaned_text'])
            if simplified and simplified != clause['cleaned_text']:
                print(f"\nSimplified: {simplified}")

            print("-" * 60)

        print(f"\n{'='*80}")
        print("SESSION SUMMARY")
        print(f"User: {username}")
        print(f"Contract: {contract_file}")
        print(f"Total Clauses Processed: {len(processed_clauses)}")
        print(f"Processing completed successfully!")
        print(f"{'='*80}")

    else:
        print("✗ Error in document extraction:", raw_text)

def save_session_info(username, clause_count):
    """Save session information for analytics"""
    session_file = os.path.join("data", "sessions.json")

    session_data = {
        "username": username,
        "timestamp": "2025-09-29",  # You can use datetime for actual timestamp
        "clauses_processed": clause_count,
        "contract_file": "Contract document.pdf"
    }

    # Load existing sessions
    if os.path.exists(session_file):
        try:
            with open(session_file, 'r') as f:
                sessions = json.load(f)
        except:
            sessions = []
    else:
        sessions = []

    # Add new session
    sessions.append(session_data)

    # Save back to file
    with open(session_file, 'w') as f:
        json.dump(sessions, f, indent=4)

# For backward compatibility - if someone runs main.py directly
if __name__ == "__main__":
    print("Please run login.py to access the Clause Ease AI system.")
    print("Default credentials:")
    print("  Username: admin, Password: admin123")
    print("  Username: user, Password: user123")
    print("  Username: sourab, Password: password123")