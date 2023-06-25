import requests

client_id = 'f6c84bcf68e94c56a26e8d38efaddc83'
client_secret = '7d265a60c6d9468d9d1670793c9d484f'
token_url = 'https://accounts.spotify.com/api/token'


def retrieve_spotify_token(client_id: str, client_secret: str, token_url: str):
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    get_token_response = requests.post(token_url, data=payload, headers=headers)

    if get_token_response.status_code == 200:
        token_data = get_token_response.json()
        access_token = token_data['access_token']
        print(f'Access Token: {access_token}')
        return access_token
    else:
        print(f'Error: {get_token_response.status_code} - {get_token_response.text}')

def retrieve_artist_info(token: str, artist_id: str):
    artist_url = 'https://api.spotify.com/v1/artists/' + artist_id
    headers = {
        'Authorization': str('Bearer ' + token)
    }

    get_artist_response = requests.get(artist_url, headers=headers)

    if get_artist_response.status_code == 200:
        artist_data = get_artist_response.json()
        print(f'Successfully retrieved {artist_data["name"]} data')
        return artist_data


token = retrieve_spotify_token(client_id, client_secret, token_url)
taco_hemingway_data = retrieve_artist_info(token, '7CJgLPEqiIRuneZSolpawQ?si=g8If1ip8TwOHuq51OElqxA')



def redirect_to_auth_code_flow(client_id: str):
    pass


def generate_code_verifier(length: str):
    pass


def generate_code_challange(code_verifier: str):
    pass


def get_access_token(client_id: str, code: str):
    pass

def fetch_profile(token: str):
    pass
