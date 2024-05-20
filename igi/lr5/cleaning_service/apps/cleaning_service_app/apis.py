import decimal

import requests


def get_current_bitcoin_price():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/USD.json'
    response = requests.get(url)
    data = response.json()
    bitcoin_price_usd = data['bpi']['USD']['rate']
    return decimal.Decimal(bitcoin_price_usd.replace(',', ''))


def get_cat_facts():
    url = 'https://catfact.ninja/fact'
    response = requests.get(url)

    return response.json()


def get_random_user_from_apis():
    url_user = "https://randomuser.me/api/"
    url_age = "ttps://api.agify.io/?name="
    response_user = requests.get(url_user)
    if response_user.status_code == 200:
        user_data = response_user.json()
        user_info = user_data['results'][0]
        response_age = requests.get(url_age + str(user_info['name']['first']))
        return {
            'last_name': user_info['name']['last'],
            'first_name': user_info['name']['first'],
            'email': user_info['email'],
            'age': response_age,
        }
    else:
        return None