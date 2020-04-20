from datetime import datetime
from app import db


class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(32), index=True, default=datetime.now().strftime("%d.%m.%Y"))
    time = db.Column(db.String(16), index=True, default=datetime.now().strftime("%H:%M:%S"))
    temperature = db.Column(db.Float, default=0)
    humidity = db.Column(db.Float, default=0)
    pressure = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<Measurement {}>'.format(self.id)

    def asDict(self):
        return ({"date" : self.date, "time" : self.time, "temperature" : self.temperature, "humidity" : self.humidity, "pressure" : self.pressure})