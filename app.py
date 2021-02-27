import os
from datetime import datetime

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)

class Honor(db.Model):
    __tablename__="code_honor"
    
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    honor = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, honor, timestamp):
        self.honor = honor
        self.timestamp = timestamp

@app.route('/webhook', methods=['POST'])
def respond():
    data = request.json
    print("recieved")
    action = data['action']
    fields = data["user"]
    if action == "honor_changed":
        honor = fields["honor"]
        new_data = Honor(honor, timestamp())
        db.session.add(new_data)
        db.session.commit()
        # write_db(query)
    return Response(status=200)


def timestamp():
    now = datetime.now()
    # return now.strftime("%Y-%m-%d %H:%M:%S+00")
    return now
