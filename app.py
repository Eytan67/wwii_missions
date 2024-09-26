import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.models import db
from blue_prints.missions_bp import mission_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(mission_bp)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello fghjklWorld!'


if __name__ == '__main__':
    app.run()
