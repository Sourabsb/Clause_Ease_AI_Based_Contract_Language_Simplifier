import streamlit as st
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ROOT_STR = str(ROOT)
SRC = str(ROOT / 'src')
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from login import LoginSystem
from components.module1_document_ingestion import extract_text
from components.module2_text_preprocessing import preprocess_contract_text
from components.module3_clause_detection import ensure_model_loaded, detect_clause_type
from components.module5_language_simplification import ensure_simplifier_loaded, simplify_text
from components.module4_legal_terms import extract_legal_terms
from scripts.download_models import download_all_models

st.set_page_config(page_title="Clause Ease AI", layout="wide")

login_sys = LoginSystem()

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['username'] = None

if not st.session_state['authenticated']:
    st.title('🔐 ClauseEase AI - Login')
    
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to your account")
        username = st.text_input('Username', key='login_username')
        password = st.text_input('Password', type='password', key='login_password')
        if st.button('Login', type='primary'):
            if login_sys.authenticate(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                st.success(f'Welcome back, {username}!')
                st.rerun()
            else:
                st.error('Invalid username or password')
    
    with tab2:
        st.subheader("Create a new account")
        new_username = st.text_input('Choose Username', key='register_username', 
                                      help='Username must be at least 3 characters')
        new_password = st.text_input('Choose Password', type='password', key='register_password',
                                      help='Password must be at least 6 characters')
        confirm_password = st.text_input('Confirm Password', type='password', key='confirm_password')
        
        if st.button('Register', type='primary'):
            # Validate passwords match
            if new_password != confirm_password:
                st.error('Passwords do not match!')
            else:
                # Attempt registration
                success, message = login_sys.register(new_username, new_password)
                if success:
                    st.success(message)
                    st.info('Please switch to the Login tab to sign in.')
                else:
                    st.error(message)
else:
    st.title('📄 Clause Ease AI - Contract Language Simplifier')
    st.markdown(f'**Logged in as:** {st.session_state["username"]}')
    if st.button('Logout'):
        st.session_state['authenticated'] = False
        st.session_state['username'] = None
        st.rerun()
    st.divider()
    uploaded_file = st.file_uploader('Upload Contract Document', type=['pdf', 'docx', 'txt'])
    if 'processing_results' not in st.session_state:
        st.session_state['processing_results'] = {}
    if uploaded_file:
        if st.button('Process Contract', type='primary'):
            temp_path = Path('temp_uploads') / uploaded_file.name
            temp_path.parent.mkdir(exist_ok=True)
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            with st.status('Module 1: Document Ingestion', expanded=True):
                st.write('Extracting text from document...')
                raw_text = extract_text(str(temp_path))
                if raw_text.startswith('[ERROR]'):
                    st.error(f'Error: {raw_text}')
                    st.stop()
                else:
                    word_count = len(raw_text.split())
                    st.session_state['processing_results']['raw_text'] = raw_text
                    st.write(f'Extracted {word_count} words')
            with st.expander('View Extracted Text'):
                st.text_area('Raw Text', raw_text, height=400)
            with st.status('Module 2: Text Preprocessing', expanded=True):
                st.write('Cleaning and segmenting text...')
                clauses = preprocess_contract_text(raw_text)
                st.session_state['processing_results']['clauses'] = clauses
                total_sentences = sum(len(c['sentences']) for c in clauses)
                total_entities = sum(len(c['entities']) for c in clauses)
                st.write(f'Found {len(clauses)} clauses')
                st.write(f'Identified {total_sentences} sentences')
                st.write(f'Extracted {total_entities} named entities')
            with st.expander('View Preprocessing Results'):
                for i, clause in enumerate(clauses, 1):
                    st.markdown(f'**Clause {i}:**')
                    st.write(f'- Sentences: {len(clause["sentences"])}')
                    st.write(f'- All Sentences:')
                    for j, sent in enumerate(clause["sentences"], 1):
                        st.write(f'  {j}. {sent}')
                    st.write(f'- Entities: {clause["entities"]}')
                    st.divider()
            with st.status('Module 3: Clause Detection', expanded=True):
                st.write('Classifying clause types...')
                print("🔄 Starting Module 3: Clause Detection")
                clause_types = []
                for clause in clauses:
                    clause_type = detect_clause_type(clause['cleaned_text'])
                    clause_types.append(clause_type)
                st.session_state['processing_results']['clause_types'] = clause_types
                from collections import Counter
                type_counts = Counter(clause_types)
                st.write(f'Classified {len(clause_types)} clauses')
                for ctype, count in type_counts.most_common():
                    st.write(f'  - {ctype}: {count}')
                print(f"✅ Module 3 complete: {len(clause_types)} clauses classified")
            with st.expander('View Clause Classifications'):
                for i, (clause, ctype) in enumerate(zip(clauses, clause_types), 1):
                    st.markdown(f'**Clause {i}:** `{ctype}`')
                    st.write(clause['cleaned_text'])
                    st.divider()
            with st.status('Module 4: Legal Terms Extraction', expanded=True):
                st.write('Extracting defined legal terms...')
                print("🔄 Starting Module 4: Legal Terms Extraction")
                all_terms = extract_legal_terms(raw_text)
                st.session_state['processing_results']['legal_terms'] = all_terms
                st.write(f'Found {len(all_terms)} legal terms')
                if all_terms and len(all_terms) > 0:
                    st.write('All terms extracted successfully')
                print(f"✅ Module 4 complete: {len(all_terms)} terms extracted")
            with st.expander('View All Legal Terms'):
                if all_terms and len(all_terms) > 0:
                    for term, category in all_terms:
                        st.markdown(f'- **{term}** ({category})')
                else:
                    st.write('No legal terms found')
            with st.status('Module 5: Language Simplification', expanded=True):
                st.write('Simplifying legal language...')
                print("🔄 Starting Module 5: Language Simplification")
                simplified_texts = []
                try:
                    for i, clause in enumerate(clauses, 1):
                        print(f"  Simplifying clause {i}/{len(clauses)}...")
                        simplified = simplify_text(clause['cleaned_text'])
                        simplified_texts.append(simplified)
                    st.session_state['processing_results']['simplified'] = simplified_texts
                    st.write(f'✅ Successfully simplified {len(simplified_texts)} clauses')
                    print(f"✅ Module 5 complete: {len(simplified_texts)} clauses simplified")
                except Exception as e:
                    st.error(f'Error during simplification: {str(e)}')
                    st.write(f'Debug info: {type(e).__name__}')
                    print(f"❌ Module 5 error: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    print(traceback.format_exc())
            with st.expander('View All Simplified Text'):
                # Show combined simplified text
                st.markdown("### 📝 Language Simplified")
                st.markdown("---")
                
                combined_simplified = ""
                for i, simplified in enumerate(simplified_texts, 1):
                    combined_simplified += f"**Clause {i}:**\n\n{simplified}\n\n"
                
                st.markdown(combined_simplified)
                st.markdown("---")
                st.info(f"✅ Total {len(simplified_texts)} clauses have been simplified")
    else:
        st.info('Upload a contract document to begin processing')
