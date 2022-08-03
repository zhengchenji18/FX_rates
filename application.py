"""
FX rate microservice
Get data from sqllite db file
serve fx rate through get_rates endpoint through GET
"""
import io
import os
from flask import Flask,jsonify,request
import pandas as pd
import yaml
from flask_sqlalchemy import SQLAlchemy
from config import create_app

application = create_app()
app = application

with io.open('db.yaml', 'r', encoding='utf8') as f:
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_yaml['db_dir'])
db = SQLAlchemy(app)


@app.route('/')
def home():
    """default function for the root dir"""
    return jsonify(message='FX_rates: I return fx rates')


@app.route('/get_rates', methods=['GET'])
def get_rates():
    """service fx rate if the date format is correct"""
    try:
        format_yyyymmdd = "%Y-%m-%d"
        date = request.args.get('date')
        date_str = pd.to_datetime(date, format=format_yyyymmdd) \
                        .strftime(format_yyyymmdd + ' 00:00:00')
        query = f'select * from fx where Date = "{date_str}"'
        df = pd.read_sql(query,db.engine)

        return df.to_json(orient='values')
    except (ValueError, AttributeError):
        return jsonify(message = 'please use format \
            http://localhost:5000/get_rates?date=2022-07-16')

if __name__ == '__main__':
    app.run()
