from dotenv import load_dotenv
from app.constants import *
import os
import uvicorn

load_dotenv()

if __name__ == '__main__':
    
    if not os.path.exists(PATH_TRASH):
        os.mkdir(PATH_TRASH)
    
    app = 'app.main:app'
    
    uvicorn.run(
        app,
        host=  os.environ.get("FASTDUP_HOST"),
        port= int(os.environ.get("FASTDUP_PORT")),
        reload= bool(int(os.getenv("DEBUG"))),
        timeout_keep_alive=None
        )