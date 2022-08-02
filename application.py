from flask import Flask, jsonify,request
import pandas as pd
import os
import sqlite3
import yaml
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
app = application
app.config['SECRET_KEY'] = 'asdfasfw12312326'


with open('db.yaml', 'r') as f:
    db_yaml = yaml.load(f, Loader=yaml.FullLoader)    
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_yaml['db_dir'])
db = SQLAlchemy(app)


@app.route('/')
def home():
	return jsonify(message='FX_rates: I return fx rates')


@app.route('/get_rates', methods=['GET']) 
def get_rates():
	date = request.args.get('date')	

	if not date:
		return jsonify(message = 'please use format http://localhost:5000/get_rates?date=2022-07-16')
	else:				
		query = f'select * from fx where Date = "{date} 00:00:00"'				
		df = pd.read_sql(query,db.engine)

		return df.to_json(orient='values')


if __name__ == '__main__':
	app.run()