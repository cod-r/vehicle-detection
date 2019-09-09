import time
import json
from flask import Flask, make_response


DEVICE_ID = 1
SURVEILLANCE_AREA = "Calea Victoriei nr. xyz"


isLaneOccupied = False
occupiedTimeElapsed = 0

app = Flask(__name__)

@app.route('/')
def hello_world():
	jsonResponse = json.dumps({
        "ID dispozitiv": DEVICE_ID,
        "Locatia supravegheata": SURVEILLANCE_AREA,
        "Pista ocupata": isLaneOccupied,
        "Timp ocupare pista": occupiedTimeElapsed
        })

	apiResponse = make_response( jsonResponse )
	apiResponse.mimetype = 'application/json'
	return apiResponse


app.run()