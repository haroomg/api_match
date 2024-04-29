from pydantic import BaseModel
from typing import Union

class Compare_texts(BaseModel):
    
    consultation: Union[dict, list] 


class Compare_img(BaseModel):
    
    url_img_1: list
    url_img_2: list