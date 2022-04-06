FROM python:3.10

LABEL PROJECT_NAME = "Variation Scraper"
LABEL OPS_AUTHOR="hoanv@daintech.com"
LABEL SRC_AUTHOR="hoanv@daintech.com"
LABEL OWNER="Daintech"

WORKDIR /code 

COPY requirements.txt  .
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT ["nohup", "python3", "main.py", ">", "server.log", "&"]