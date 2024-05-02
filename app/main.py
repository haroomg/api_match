from .schemas import TextComparation, TextListComparation, ImageComparation
from .funtions import format, compare_img
from fastapi import FastAPI, Body
from typing import Union, List
from fuzzywuzzy import fuzz

app = FastAPI()

@app.post('/compare/text')
async def compare_text_api(items: TextListComparation):
    
    def calculate_similarity(str1: str, str2: str) -> int:
        return fuzz.ratio(str1, str2)
    
    def preprocessed(item: dict):
        
        id_ = item.id
        string_1 = format(item.string_1)
        string_2 = format(item.string_2) 
        
        similarity = calculate_similarity(string_1, string_2)
        
        internal_result = {
            'id': id_,
            'similarity': similarity
            }
        
        return internal_result
    
    data = items.data
    result = []
    
    for item in data:
        
        result.append(
            preprocessed(item)
        )
    
    return result


@app.post('/compare/img')
def compare_img_api(request: ImageComparation):
    
    url_img_1: list = request.url_img_1
    url_img_2: list = request.url_img_2
    
    result = compare_img(url_img_1, url_img_2)
    
    print(result)
    
    return result