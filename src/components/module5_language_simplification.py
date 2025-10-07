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
            print("Using Hugging Face token from environment")
        
        _simplifier = pipeline("summarization", model=model_name, **kwargs)
        print(f"Loaded simplification model: {model_name}")
        return True
    except Exception as e:
        print(f"Failed to load simplifier: {e}")
        _simplifier = None
        return False


def simplify_text(text: str, max_length=60):
    global _simplifier, _load_attempted
    
    if not text or not text.strip():
        return text
    
    if _HAS_HF and _simplifier is None and not _load_attempted:
        print("🔄 Auto-loading AI simplification model (facebook/bart-large-cnn)...")
        ensure_simplifier_loaded("facebook/bart-large-cnn")
    
    if _simplifier and len(text.split()) > 10:
        try:
            from nltk.tokenize import sent_tokenize
            sentences = sent_tokenize(text)
            
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
            return text
    
    return text
