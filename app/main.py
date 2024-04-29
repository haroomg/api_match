from .schemas import Compare_texts, Compare_img
from fastapi import FastAPI
from .funtions import *

app = FastAPI()

@app.post('/compare/text')
def compare_text_api(request: Compare_texts) -> dict:
    
    consultation = request.consultation
    
    return compare_text(consultation)


@app.post('/compare/img')
def compare_img_api(request: Compare_img) -> dict:
    
    url_img_1: list = request.url_img_1
    url_img_2: list = request.url_img_2
    
    return compare_img()