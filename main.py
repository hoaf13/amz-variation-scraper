from email import header
from http.client import HTTPException
from itertools import product
from math import prod
import os 
import pathlib
import string
from urllib import request
from urllib.error import ContentTooShortError

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

# ENDPOINT
@app.post("/api/v1/get_variation_information")
async def get_variation_information(file: UploadFile, token: str = Depends(token_auth_scheme)):    
    if token.credentials != TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not valid token",
            headers={"WWW-Authenticate": "Basic"},
        )
    content = file.file.read().decode("utf-8")
    scraper = VariationScraper()
    data = scraper.get_information(web_content=content)
    status_crawler = data["status"]
    del data["status"]
    res = {
        "status": status_crawler,
        "data": data
    }
    return res

if __name__ == "__main__":    
    uvicorn.run(app=APP, host=HOST, port=PORT,workers=WORKER_NUMBER)