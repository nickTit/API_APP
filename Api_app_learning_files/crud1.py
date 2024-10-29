import sys
sys.path.append('/home/redmi/Python_test_tasks/API_APP/')
sys.path.append('/home/redmi/Python_test_tasks/API_APP/database/')

import datetime
import pydantic_models1
import models
import bit
#from [API_APP].config import *
#import config
import config
wallet = bit.PrivateKeyTestnet(config.a)  # создание кошелька
print(wallet.get_balance())
print(f"Адрес: {wallet.address}")
print(f"Приватный ключ: {wallet.to_wif()}")