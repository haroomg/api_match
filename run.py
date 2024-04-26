from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import FastAPI
from fuzzywuzzy import fuzz
from uuid import uuid4
import requests
import uvicorn
import fastdup
import os
import re

load_dotenv()

app = FastAPI()
PATH_TRASH = 'trash'

class Compare_texts(BaseModel):
    
    string_1: str
    string_2: str


class Compare_img(BaseModel):
    
    url_img_1: list
    url_img_2: list

############################### Funtions - start:
def format(data: str) -> str:
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                    "]+", re.UNICODE)
    return re.sub(emoj, '', data).lower()

def download_img(url: str, path: str) -> bool:
    
    _, file_name = os.path.split(url)
    file_path = os.path.join(path, file_name)
    response = requests.get(url)
    
    if response.status_code == 200:
        
        with open(file_path, "wb") as archivo:
            archivo.write(response.content)
            
        return True
    else:
        return False
    
############################### Funtions - end

@app.post('/compare/text')
def compare_text(request: Compare_texts) -> dict:
    
    string_1: str = format(request.string_1)
    string_2: str = format(request.string_2)
    
    similarity_score: int = fuzz.ratio(string_1, string_2)
    
    result: dict = {
        'similarity': similarity_score
    }
    
    return result


@app.post('/compare/img')
def compare_img(request: Compare_img) -> dict:
    
    url_img_1: list = request.url_img_1
    url_img_2: list = request.url_img_2
    
    direction_name = str(uuid4())
    path_images = os.path.join(PATH_TRASH, direction_name)
    os.mkdir(path_images)
    
    cont_images1 = 0
    cont_images2 = 0
    
    for img1, img2 in zip(url_img_1, url_img_2):
        
        if download_img(img1, path_images):
            cont_images1 += 1
        
        if download_img(img2, path_images):
            cont_images2 += 1
    else:
        if cont_images1 == 0 or cont_images2 == 0:
            # aqui tienes que terminar de controlar este error
            msm_error = {}
    
    fd = fastdup.create(input_dir=path_images, work_dir=path_images)
    fd.run()
    
    result = fd.similarity()

if __name__ == '__main__':
    
    if not os.path.exists(PATH_TRASH):
        os.mkdir(PATH_TRASH)
    
    uvicorn.run(
        'run:app',
        host=  os.environ.get("FASTDUP_HOST"),
        port= int(os.environ.get("FASTDUP_PORT")),
        reload= bool(int(os.getenv("DEBUG"))),
        timeout_keep_alive=None
        )