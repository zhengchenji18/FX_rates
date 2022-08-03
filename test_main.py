from application import create_app
from flask import Flask

def test_rate(client):
    app = Flask(__name__)
    client = app.test_client()    
    url = '/'
    #url = '/get_rates?date=2022-07-15'
    response = client.get(url)
    assert response.status_code == 200