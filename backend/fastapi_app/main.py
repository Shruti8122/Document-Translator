from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import config
from .ocr_engine import ocr_image
from .translator import translate_text

app = FastAPI(title="Doc Translator Inference API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslateRequest(BaseModel):
    text: str
    target_lang: str


class TranslateResponse(BaseModel):
    translated_text: str


class OCRResponse(BaseModel):
    text: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/languages")
def get_languages():
    return {
        name: codes
        for name, codes in config.LANGUAGE_MAP.items()
    }


@app.post("/api/ocr", response_model=OCRResponse)
async def ocr_endpoint(file: UploadFile = File(...), source_lang: str = "en"):
    if source_lang not in {v["easyocr"] for v in config.LANGUAGE_MAP.values()}:
        codes = [v["easyocr"] for v in config.LANGUAGE_MAP.values()]
        if source_lang not in codes:
            source_lang = "en"
    contents = await file.read()
    try:
        text = ocr_image(contents, [source_lang])
        return OCRResponse(text=text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/translate", response_model=TranslateResponse)
async def translate_endpoint(req: TranslateRequest):
    target = req.target_lang
    valid_codes = {v["nllb"] for v in config.LANGUAGE_MAP.values()}
    if target not in valid_codes:
        raise HTTPException(status_code=400, detail=f"Unsupported target language code: {target}")
    try:
        result = translate_text(req.text, target)
        return TranslateResponse(translated_text=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.HOST, port=config.PORT)
