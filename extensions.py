import requests
import json

class APIException(Exception):
    def __init__(self,  *args): 
        self.args = args[0]
        self.callback = args[1]

        self.callback(self.__str__())   

    def __str__(self):
        if (len(self.args)>1):
            return f"There was an API Exception while converting {self.args[1]}"
        return "There are no arguments provided.\n Provide <base> <target> <amount>"
        
class APIRequester():

    __apiKey = json.load(open('config.json'))["API_KEY"]
    __URL = f'https://v6.exchangerate-api.com/v6/{__apiKey}/pair'

    @staticmethod 
    def get_price(base, quote, amount):
        if(APIRequester.__apiKey == None):
            raise RuntimeError()
        
        URL = APIRequester.__URL+ f'/{base}/{quote}'
        request = requests.get(URL)
        response_quote = request.json()["conversion_rate"]
        return float(response_quote)*float(amount)
