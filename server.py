import time
import json
from flask import Flask, make_response

app = Flask(__name__)

@app.route('/')
def get_surveillance_details():

    with open('data.json', encoding='utf-8') as f:
        jsonResponse = json.load(f)



    apiResponse = make_response(jsonResponse)
    apiResponse.mimetype = 'application/json'

    return apiResponse

# # with open('data.json', 'w', encoding='utf-8') as f:
# #     json.dump(jsonResponse, f, ensure_ascii=False, indent=4)

    
# with open('data.json', encoding='utf-8') as f:
#     datele = json.load(f)
#     print(datele)



app.run(host='0.0.0.0')