from typing import List, Optional
from pydantic import BaseModel
from typing import Union

class TextComparation(BaseModel):
    
    id: int
    string_1: str
    string_2: str


class TextListComparation(BaseModel):
    
    data: List[TextComparation]

class ImageComparation(BaseModel):
    
    url_img_1: list
    url_img_2: list
    