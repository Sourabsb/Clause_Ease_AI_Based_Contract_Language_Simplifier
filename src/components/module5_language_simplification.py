# Try to import transformers
import os
from pathlib import Path

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    _HAS_HF = True
except Exception:
    _HAS_HF = False

try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from {env_path}")
except ImportError:
    print("⚠ python-dotenv not installed, skipping .env loading")
    pass

HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")

_simplifier = None
_load_attempted = False


def ensure_simplifier_loaded(model_name="facebook/bart-large-cnn"):
    global _simplifier, _load_attempted
    
    if _load_attempted:
        return _simplifier is not None
    
    _load_attempted = True
    
    if not _HAS_HF:
        return False
    try:
        kwargs = {"use_fast": False}
        if HF_TOKEN:
            kwargs["token"] = HF_TOKEN
            print("🔐 Using Hugging Face token from environment")
        
        _simplifier = pipeline("summarization", model=model_name, **kwargs)
        print(f"✅ Loaded simplification model: {model_name}")
        return True
    except Exception as e:
        print(f"❌ Failed to load simplifier: {e}")
        _simplifier = None
        return False


_LEGALESE_REPLACEMENTS = [
    # Very long phrases
    ("which expression shall unless repugnant to the context or meaning thereof include its successors and permitted assigns", "which includes its future owners"),
    ("which expression shall unless repugnant to the context or meaning thereof include their respective successors and permitted assigns", "which includes their future owners"),
    ("shall be deemed to form and be read and construed as integral part of this agreement", "will be considered part of this agreement"),
    ("shall be deemed to form and be read and construed as part of this agreement", "will be considered part of this agreement"),
    ("in consideration of the payments to be made by the employer to the contractor", "in exchange for payment by the employer to the contractor"),
    ("at the times and in the manner prescribed by the contract", "as required by the contract"),
    ("notwithstanding anything to the contrary", "despite anything else"),
    
    # Long phrases
    ("hereinafter referred to as the", "called the"),
    ("hereinafter referred to as", "called"),
    ("which expression shall unless repugnant", "which unless conflicting"),
    ("shall unless repugnant to the context or meaning thereof include", "will include"),
    ("unless repugnant to the context or meaning thereof", "unless conflicting"),
    ("successors and permitted assigns of the one part", "future owners"),
    ("successors and permitted assigns of the other part", "future owners"),
    ("successors and permitted assigns", "future owners"),
    ("permitted assigns", "authorized successors"),
    ("has accepted the bid submitted by the contractor", "has accepted the contractor's bid"),
    ("is desirous that the contractor executes", "wants the contractor to complete"),
    ("the contractor hereby covenants and agrees with the employer", "the contractor promises the employer"),
    ("the employer hereby covenants and agrees", "the employer promises"),
    ("witnesseth as follows", "confirms the following"),
    ("in witness whereof the parties hereto have executed this agreement", "to confirm this, the parties have signed this agreement"),
    ("in witness whereof", "to confirm this"),
    ("executed this agreement on the day month and year first written", "signed this agreement on the date mentioned"),
    ("executed this agreement", "signed this agreement"),
    ("the common seal of both the parties is hereunto affixed", "both parties have officially sealed this"),
    ("signed sealed and delivered by the said parties", "signed and delivered by the parties"),
    
    ("is made on", "is dated"),
    ("having its registered office at", "with office at"),
    ("for the execution and completion of such works", "to complete such works"),
    ("and the remedying of any defects therein", "and fix any defects"),
    ("at a accepted contract amount of", "for a contract amount of"),
    ("words and expression shall assume the same meanings", "words will have the same meanings"),
    ("are respectively assigned to them in", "are given in"),
    ("in conformity in all respects with", "following"),
    ("shall undertake ensure and process", "will ensure"),
    ("within the time for completion", "by the deadline"),
    ("to achieve the milestones within the time prescribed thereof", "to meet the milestones on time"),
    ("at the times and in the manner prescribed", "as required"),
    ("in the presence of", "witnessed by"),
    ("on behalf of", "representing"),
    
    ("hereinafter", "from now on"),
    ("herein", "in this document"),
    ("hereby", "by this"),
    ("hereto", "to this"),
    ("thereof", "of it"),
    ("therein", "in it"),
    ("thereto", "to it"),
    ("hereunto", "to this"),
    ("aforementioned", "mentioned above"),
    ("aforesaid", "said above"),
    ("forthwith", "immediately"),
    ("prior to", "before"),
    ("subsequent to", "after"),
    ("in the event that", "if"),
    ("pursuant to", "according to"),
    ("in accordance with", "following"),
    ("with respect to", "about"),
    ("in consideration of", "in exchange for"),
    ("integral part", "part"),
    ("prevail over", "take priority over"),
    ("deemed to be", "considered"),
    ("deemed to form", "considered as"),
    ("construed as", "understood as"),
    ("repugnant to", "conflicting with"),
    ("the said", "the"),
    ("affixed", "attached"),
    
    ("shall", "will"),
    ("whereas", "since"),
    ("executes", "completes"),
    ("undertakes", "agrees to"),
    ("covenants", "promises"),
    ("representations", "statements"),
    ("acknowledges", "agrees"),
    ("desirous", "wants"),
    ("witnesseth", "confirms"),
]


def _rule_based_simplify(text: str) -> str:
    import re
    
    if not text or not text.strip():
        return text
    
    s = text
    original_length = len(s)
    
    s = re.sub(r'\.{3,}', '[___]', s)
    
    replacements_made = 0
    for old, new in _LEGALESE_REPLACEMENTS:
        if old.lower() in s.lower():
            s = re.sub(re.escape(old), new, s, flags=re.IGNORECASE)
            replacements_made += 1
    
    s = re.sub(r'\bthe\s+the\b', 'the', s, flags=re.IGNORECASE)
    
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([.,;:])', r'\1', s)
    s = s.strip()
    
    if replacements_made > 0:
        print(f"    → Made {replacements_made} replacements, length {original_length} → {len(s)}")
    
    return s


def simplify_text(text: str, max_length=60):
    global _simplifier, _load_attempted
    
    if not text or not text.strip():
        return text
    
    if _HAS_HF and _simplifier is None and not _load_attempted:
        print("🔄 Auto-loading AI simplification model (facebook/bart-large-cnn)...")
        ensure_simplifier_loaded("facebook/bart-large-cnn")
    
    preprocessed = _rule_based_simplify(text)
    
    if _simplifier and len(preprocessed.split()) > 10:
        try:
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(preprocessed)
            
            simplified_sentences = []
            for sent in sentences:
                if len(sent.strip()) < 20:
                    simplified_sentences.append(sent)
                    continue
                
                try:
                    sent_words = len(sent.split())
                    dynamic_max_length = max(15, min(int(sent_words * 0.7), 50))
                    
                    result = _simplifier(
                        sent, 
                        max_length=dynamic_max_length, 
                        min_length=10,
                        do_sample=False,
                        truncation=True
                    )
                    
                    if result and len(result) > 0 and 'summary_text' in result[0]:
                        ai_output = result[0]['summary_text'].strip()
                        if len(ai_output) > 5 and len(ai_output) <= len(sent) * 1.5:
                            simplified_sentences.append(ai_output)
                        else:
                            simplified_sentences.append(sent)
                    else:
                        simplified_sentences.append(sent)
                        
                except Exception as e:
                    simplified_sentences.append(sent)
            
            return ' '.join(simplified_sentences)
            
        except Exception as e:
            print(f"⚠ AI simplification failed: {e}")
            return preprocessed
    
    return preprocessed
