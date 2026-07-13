import re

_model = None
_tokenizer = None


def get_model():
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        _tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        _model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
    return _model, _tokenizer


def _chunk_text(text: str, tokenizer, max_tokens: int = 450) -> list:
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current = []
    current_tokens = 0
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_tokens = len(tokenizer.encode(para))
        if para_tokens > max_tokens:
            if current:
                chunks.append("\n\n".join(current))
                current, current_tokens = [], 0
            sentences = re.split(r"(?<=[.!?\u3002\uff01\uff1f])\s*", para)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                sent_tokens = len(tokenizer.encode(sent))
                if current_tokens + sent_tokens > max_tokens and current:
                    chunks.append(" ".join(current))
                    current, current_tokens = [sent], sent_tokens
                else:
                    current.append(sent)
                    current_tokens += sent_tokens
            if current:
                chunks.append(" ".join(current))
                current, current_tokens = [], 0
        elif current_tokens + para_tokens > max_tokens and current:
            chunks.append("\n\n".join(current))
            current, current_tokens = [para], para_tokens
        else:
            current.append(para)
            current_tokens += para_tokens
    if current:
        chunks.append("\n\n".join(current))
    return chunks if chunks else [text]


def translate_text(text: str, target_lang_code: str) -> str:
    model, tokenizer = get_model()
    chunks = _chunk_text(text, tokenizer)
    translated_chunks = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", padding=True, truncation=True, max_length=512)
        forced_bos_token_id = tokenizer.lang_code_to_id[target_lang_code]
        outputs = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=512,
            num_beams=4,
            early_stopping=True,
        )
        translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        translated_chunks.append(translated)
    return "\n\n".join(translated_chunks)
