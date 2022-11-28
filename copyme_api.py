from fastapi import FastAPI, HTTPException
from copyme import generate_copy_snippet, generate_keywords, generate_synonyms

app = FastAPI()

MAX_INPUT_LENGTH = 32


@app.get("/generate_snippet")
async def generate_snippet_api(prompt: str):
    snippet = generate_copy_snippet(prompt)
    return {"snippet": snippet, "keywords": [], "synonyms": []}


@app.get("/generate_keywords")
async def generate_keywords_api(prompt: str):
    keywords = generate_keywords(prompt)
    return {"snippet": None, "keywords": keywords, "synonyms": []}


@app.get("/generate_synonyms")
async def generate_synonyms_api(prompt: str):
    synonyms = generate_synonyms(prompt)
    return {"snippet": None, "keywords": [], "synonyms": synonyms}


@app.get("/generate_snippet_keywords_synonyms")
async def generate_synonyms_api(prompt: str):
    validate_input_length(prompt)
    snippet = generate_copy_snippet(prompt)
    keywords = generate_keywords(prompt)
    synonyms = generate_synonyms(prompt)
    return {"snippet": snippet, "keywords": keywords, "synonyms": synonyms}


def validate_input_length(prompt: str):
    if len(prompt) >= MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400, detail=f"Input length is too long. Must be under {MAX_INPUT_LENGTH} characters")
