from .constants import PATH_TRASH
import concurrent.futures
from shutil import rmtree
from uuid import uuid4
import requests
import fastdup
import os, re

###############################
# functions that support other:

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


def download_imgs(urls: list, path: str) -> list:
    
    def download_img(url: str, path: str) -> bool:
    
        _, file_name = os.path.split(url)
        file_path = os.path.join(path, file_name)
        response = requests.get(url)
        
        if response.status_code == 200:
            
            with open(file_path, "wb") as archivo:
                archivo.write(response.content)
                
            return file_name, True
        else:
            return file_name, False
        
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        
        futures = [executor.submit(download_img, url, path) for url in urls]
        
        for future in concurrent.futures.as_completed(futures):
            
            file_name, result =future.result()
            results[file_name] = result
            
    return results

############################### end


def compare_img(url_img_1: list = None, url_img_2: list = None) -> dict:
    
    direction_name = str(uuid4())
    
    new_path = os.path.join(PATH_TRASH, direction_name)
    os.mkdir(new_path)
    
    path_images = os.path.join(new_path, 'img')
    os.mkdir(path_images)
    
    path_fastdup = os.path.join(new_path, 'fastdup')
    os.mkdir(path_fastdup)
    
    img_1_result = download_imgs(url_img_1, path_images)
    img_2_result = download_imgs(url_img_2, path_images)
    
    if not all(img_1_result.values()) or not all(img_2_result.values()):
        
        msm_error = {}
        
        return msm_error
    
    fd = fastdup.create(input_dir=path_images, work_dir=path_fastdup)
    fd.run()
    
    similarity = fd.similarity()
    
    # cambiamos el la direccion de las imagenes para que solo sea el nombre del archivo
    for col_name, img_result in zip(["filename_from", "filename_to"], [img_1_result, img_2_result]): 
        similarity[col_name] = similarity[col_name].apply(lambda x : os.path.basename(x))
        
        similarity = similarity[similarity[col_name].isin(img_result)]
    
    rmtree(new_path)
    
    if similarity.shape[0]:
    
        result = {
            'mean': similarity['distance'].mean(),
            'max': similarity['distance'].max(),
            'min': similarity['distance'].min()
        }
        
    else:
        
        result = {
            'mean': 0,
            'max': 0,
            'min': 0
        }
    
    return result