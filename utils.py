
import os
import dotenv
import requests
from datetime import datetime

RESPONSE_REQUIRED_KEYS = ('access_token', 'refresh_token', 'expires_at')
REDIRECT_URI = 'https%3A%2F%2Flocalhost.com%3A5000%2Fstrava_oauth'


def strava_oauth(code):
    ''' Send POST request to Strava to get access_token '''
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    # post_url = f'https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code?redirect_uri={REDIRECT_URI}'
    post_url = f'https://www.strava.com/oauth/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code'
    try:
        r = requests.post(post_url)
        response = r.json()
        import pprint
        print('SUCCES')
        pprint.pprint(response)
        # filter out unneccessary items from response
        # NOTE: athlete info is also in response

        store_to_env_d = {key: value for key, value in response.items() if key in RESPONSE_REQUIRED_KEYS}
        # breakpoint()
        if not store_to_env_d:
            raise Exception('Nothing in authentication response!')  # noqa

        update_env(store_to_env_d, dotenv_file)
    except Exception as e:
        print(e)


def update_env(resp_d: dict, dotenv_file):
    ''' Update access_token, refresh_token, expires_at in env '''
    assert RESPONSE_REQUIRED_KEYS not in resp_d

    for key, value in resp_d.items():
        if value:
            value = str(value)
            os.environ[key] = value
            # set_key doesn't update os.environ
            dotenv.set_key(dotenv_file, key, value)
    # keep log of last update time
    dotenv.set_key(dotenv_file, 'updated_at', str(datetime.now()))
