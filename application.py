from flask import Flask, jsonify,request
application = Flask(__name__)
app = application


@app.route('/')
def home():
	return jsonify(message='FX_rates: I return fx rates')


@app.route('/get_rates') 
def get_rates():
	date = request.args.get('date')

	if not date:
		return jsonify(message = 'please use format http://localhost:5000/get_rates?date=2022-07-16')
	else:
		return jsonify('rates' + date)


if __name__ == '__main__':
	app.run()