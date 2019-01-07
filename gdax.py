import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase

system_name = "Crypto15"

class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or b'').decode()
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode(), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode()

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request


def call_api_request(request):
    with open('user_account.json') as json_data:
        user_account = json.load(json_data)
    api_url = 'https://api.gdax.com/'
    auth = CoinbaseExchangeAuth(user_account['API_KEY'], user_account['API_SECRET'], user_account['API_PASS'])
    return requests.get(api_url + request, auth=auth).json()


def get_user_name():
    with open('user_account.json') as json_data:
        user_account = json.load(json_data)
    return user_account['NAME']


def is_account_valid():
    valid_response = call_api_request('accounts')
    try:
        valid_response['message']
    except TypeError:
        return True
    else:
        return False


def get_account_balance():
    account_response = call_api_request('accounts')
    print("{}: Here is your balance details".format(system_name))
    print("====")
    for currency_detail in account_response:
        if (float(currency_detail['balance']) > 0 ):
            print("Currency: {}".format(currency_detail['currency']))
            print("Balance: {}".format(currency_detail['balance']))
            print("Hold: {}".format(currency_detail['hold']))
            print("Available: {}".format(currency_detail['available']))
            print("====")