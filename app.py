from flask import Flask
from flask import request
import dotenv

from flask import render_template
from datetime import datetime

from utils import strava_oauth as strava_oauth_func


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')
    # return 'Welcome to my home page!'


@app.route('/strava_oauth')
def strava_oauth():
    args = request.args
    code = args.get('code')
    response_text = 'Welcome to my page!'

    if code:
        strava_oauth_func(code)
        response_text = f'Authentication Success: {code}'

    return response_text


if __name__ == '__main__':
    # use `python app.py` in order to run below code
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    app.run(host=('0.0.0.0'), port=5001)

