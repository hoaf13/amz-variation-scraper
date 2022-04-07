from locale import normalize
from bs4 import BeautifulSoup
import requests
import re 
import json 
import itertools

class VariationScraper:
    def __init__(self):
        """
            The aim is regex required fields which related to Product in javascript files
            Explaintation: Cause dynamic page do not show ASIN code of all products so we must
            save all files related to page and catch the keys in json fields were reponsed by script.
        """
        self.scraping_patterns = [
                    r"\"currentAsin\" : \"[A-Z0-9]{10}\"", 
                    r"\"parentAsin\" : \"[A-Z0-9]{10}\"", 
                    r"\"selected_variations\" : {.*}",  # variations in current Product
                    r"\"variationValues\" : {.*}", # list all variation in currrnt Product
                    r"\"dimensionValuesDisplayData\" : {.*}" #list all Asin code and their variations
                ]

    """
        params:
        - text: in format 'key' : 'value' after regex
    """
    def normalize_text(self, text: str):
        line_string = text.strip()
        line_string = line_string[:-1] if line_string[-1] in [',',';']  else line_string 
        return line_string

    """
        params:
        - text: in format 'key' : 'value' after regex
    """        
    def parse_pair_to_dict(self, text: str):
        text = "{" + text + "}"
        data = json.loads(text)
        return data

    """ 
    scraping information from url which has detail Product
    """
    def get_information(self, web_content: str):
        try:
            print("web_content:", len(web_content))
            res = {"status":"success"}
            for pattern in self.scraping_patterns:
                match = re.search(pattern, web_content)
                print("match: ", match)
                if match:
                    line_string = match.group()
                    line_string = line_string.strip()
                    line_string = line_string[:-1] if line_string[-1] in [',',';']  else line_string 
                    line_string = "{" + line_string + "}"
                    json_data = json.loads(line_string)
                    res.update(json_data)
                    print("json_data", json_data)
            variationKeys = list(res['variationValues'])
            variationValues = list([values for key, values in res["variationValues"].items()])
            all_of_variations = list(itertools.product(*variationValues))
            all_of_variations = [list(list(value)) for value in all_of_variations]
            exisited_variations = [list(list(value)) for key, value in res['dimensionValuesDisplayData'].items()]
            not_existed_variations = [element for element in all_of_variations if element not in exisited_variations]
            res.update({"all_of_variations": all_of_variations, "not_existed_variations": not_existed_variations})

            if len(res["variationValues"]) == 1:
                return  {
                    "status": "fail",
                    "message": "This product has only a varation."
                }
            return res
        except Exception as e:
            print(f"Exception happens: {e}")
            return {
                "status": "fail",
                "message": str(e)
            }
