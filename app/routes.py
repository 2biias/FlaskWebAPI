from flask import request, redirect
from app import app, db
from app.models import Measurement
import json
from collections import namedtuple

@app.route('/')
def index():
    return "/upload to post measurement. /loadnewest to get newest measurement. /loadall to get all measurements. /loadbydate/date to load data from a date"

# Route for uploading
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        if request.is_json:
            jsonraw = request.get_json()
            # Parsing jsonfile
            MeasurementObj = jsondecoder(jsonraw)
            if MeasurementObj is not None:
                # Adding Measurement to database
                db.session.add(MeasurementObj)
                db.session.commit()
                return "Measurement added to database"
        return "Bad json"
    else:
        return redirect('/')

def jsondecoder(jsonFile):
    if 'Measurement' in jsonFile:
        jsObj = jsonFile.get('Measurement')

        MeasurementObj = Measurement(date=jsObj.get('date'), time=jsObj.get('time')\
            ,temperature=jsObj.get('temperature'), humidity=jsObj.get('humidity')\
            ,pressure=jsObj.get('pressure'))
        return MeasurementObj
    else:
        return None


# Route for getting newest data
@app.route('/loadnewest', methods=['GET'])
def loadnewest():
    newest = Measurement.query.order_by(Measurement.id.desc()).first()
    if newest:
        return json.dumps(newest.asDict())
    else:
        return "No measurements available"

# Route for getting all data
@app.route('/loadall', methods=['GET'])
def loadall():
    Measurements = Measurement.query.order_by(Measurement.id.desc()).all()
    if Measurements:
        collected = ""
        for thatMeasurement in Measurements:
            collected = collected + json.dumps(thatMeasurement.asDict()) + '\n'
        
        return collected
    else:
        return "No measuresments available"

# Route for getting data by date
@app.route('/loadbydate/<date>', methods=['GET'])
def loadbydate(date):
    print(date)
    collected = ""
    Measurements = Measurement.query.all()
    if Measurements is not None:
        for thatMeasurement in Measurements:
            if thatMeasurement.date == date:
                collected = collected + json.dumps(thatMeasurement.asDict()) + '\n'
        if collected != "":
            return collected
        else:
            "No measurement with that date"
    else:
        return "No measurements available"

# Route for clearing all measurements
@app.route('/clearall', methods=['GET'])
def clearall():
    Measurements = Measurement.query.all()
    if Measurements is not None:
        for thatMeasurement in Measurements:
            db.session.delete(thatMeasurement)
        db.session.commit()
        return "All measurements cleared"
    else:
        return "No measurements to delete"