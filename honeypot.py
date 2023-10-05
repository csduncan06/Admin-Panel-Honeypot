import requests
import json

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__, template_folder="html")

LOGFILE = 'logs.txt'

def get_location(ip_addr):
    response = requests.get(f"http://ip-api.com/json/{ip_addr}")
    data = response.json()
    country = data['countryCode']
    city = data['city']
    location = f'{country}, {city}'
    return location

def get_client_ip():
    return request.remote_addr

def current_dnt():
    dnt = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return dnt

@app.route('/')
def home():
    client_ip = get_client_ip()
    user_agent = request.headers.get('User-Agent')
    time = current_dnt()
    location = get_location(client_ip)
    with open(LOGFILE, 'a') as log_file:
        log_file.write(f'[{time}] {client_ip} {location} {user_agent}\n')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)

