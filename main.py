from email import header
from http.client import HTTPException
from itertools import product
from math import prod
import os 
import pathlib
import string
from urllib import request

from fastapi import Depends, FastAPI, UploadFile, File, status, HTTPException 
from fastapi.security import HTTPBearer  
from pydantic import BaseModel
import uvicorn
import time
import requests

from variation_scraper.scraper import VariationScraper
from config import * 


app = FastAPI()
token_auth_scheme = HTTPBearer()  

class Product(BaseModel):
    product_url: str

# remove all files in folder 
import os, shutil
folder = 'html_responses/'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# ENDPOINT
@app.post("/api/v1/get_variation_information")
async def get_variation_information(product: Product, token: str = Depends(token_auth_scheme)):    
    pid = os.getpid()
    HEADERS = ({'User-Agent': "Chrome/44.0.2403.157", 'Accept-Language': 'en-US, en;q=0.5'}) 
    response = requests.post(url=product.product_url, headers=HEADERS)
    f = open(f"html_responses/{pid}.html", 'w')
    f.write(response.text)
    f.close()
    if token.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
            headers={"WWW-Authenticate": "Basic"},
        )
    scraper = VariationScraper()
    content = response.text 
    data = scraper.get_information(web_content=content)
    status_crawler = data["status"]
    del data["status"]
    res = {
        "status": status_crawler,
        "data": data,
        "content": response.text
    }
    print("PID: {pid} - result: {res}")
    return res

if __name__ == "__main__":    
    uvicorn.run(app=APP, host=HOST, port=PORT,workers=WORKER_NUMBER)