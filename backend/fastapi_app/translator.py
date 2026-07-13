_model = None
_tokenizer = None


def get_model():
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        _tokenizer = AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
        _model = AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
    return _model, _tokenizer


def translate_text(text: str, target_lang_code: str) -> str:
    model, tokenizer = get_model()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    forced_bos_token_id = tokenizer.lang_code_to_id[target_lang_code]
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=512,
        num_beams=4,
        early_stopping=True,
    )
    translated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated
