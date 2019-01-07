import json, requests, gdax

system_name = "Crypto15"
template_menu = " or say 'menu' to return to menu\nYou: "


def print_template(what_to_say):
    print("{}: {}".format(system_name, what_to_say))


def crypto_price(crypto_name):
    crypto_name = crypto_name.upper()
    currency = 'EUR'
    response = requests.get('https://min-api.cryptocompare.com/data/price?fsym={}&tsyms={}'.format(crypto_name, currency)).json()
    try:
        response[currency]
    except KeyError:
        print_template("Never heard of {}.".format(crypto_name))
    else:
        print_template("I found your crypto price. {} is {} {} at the moment.".format(crypto_name, response[currency], currency))


def template_crypto_price():
    crypto_name = input("{}: What crypto do you want to know?{}".format(system_name, template_menu))
    if (crypto_name == 'menu'):
        template_would_you_like()
    else:
        crypto_price(crypto_name)
        template_crypto_price()


def template_would_you_like():
    option = input("{}: Would you like to 'trade', 'check price', 'check balance' or 'quit' ?\nYou: ".format(system_name))
    if (str(option) == "trade"):
        #TODO
        print("you choose trading")
    elif (str(option) == "check price"):
        template_crypto_price()
    elif (str(option) == "check balance"):
        gdax.get_account_balance()
        template_would_you_like()
    elif(str(option) == "quit"):
        print_template("Thank you for using {}. Bye for now {}!".format(system_name,gdax.get_user_name()))
    else:
        print_template("Hmmm sorry {}, what do you mean??".format(gdax.get_user_name()))
        template_would_you_like()


if __name__ == '__main__':
    if(gdax.is_account_valid() == True):
        print_template("Hi {}, welcome to {} The Crypto Currency Personal Assistant".format(gdax.get_user_name(), system_name))
        template_would_you_like()

    else:
        #TODO
        print_template("Hi there, welcome to {} The Crypto Currency Personal Assistant, please press enter to start registration")