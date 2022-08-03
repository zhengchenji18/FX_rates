from application import create_app
from flask import Flask

def test_rate(client):
    app = Flask(__name__)
    client = app.test_client()    
    url = '/'
    response = client.get(url)
    assert response.status_code == 200