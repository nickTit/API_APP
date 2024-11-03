
import copy
from select import select
import sys

sys.path.append('/home/redmi/Python_test_tasks/API_APP/database/')

from pony.orm import db_session
from requests import Request
#from database import models
from database import models
from database import crud
import pydantic_models

import fastapi
from pydantic_models import User_to_create

api = fastapi.FastAPI()



@api.get('/user/get_info_byID/{user_id:int}')
@crud.db_session
def get_info_about_user(user_id):
    return crud.get_user_info(crud.User[user_id])

@api.get('/user/get_info_byTg_ID/{tg_id:int}')
@crud.db_session
def get_info_about_user_еп(tg_id:int):
    user = crud.get_user_by_tg_id(tg_id)
    return user


@api.get('/user/get_balance_by_id/{user_id:int}')
@crud.db_session
def get_balance(user_id):
    crud.update_wallet_balance(crud.User[user_id].wallet)
    return crud.User[user_id].wallet.balance

@api.post("/user/create")
@crud.db_session
def creation_user(user: User_to_create):  #смотрим чтобы входные данные соответствовали модели типов данных класса User
    crud.create_user(user.tg_ID, user.nick).to_dict()
    return True

@api.put('/user/update/{user_id}')
def update_user(user: pydantic_models.User_to_update = fastapi.Body()):
#чисто можно передать даже айдишник,
# тк в моделях пайдентик указано хоть всё путое
# кроме айди, и тогда оно просто
# дальше в json пойдет в crud и тоже проверится через пайдентик
# и на выходе даст json
    """
фастапи сам понимаетг,
как достать данные из JSONa в теле, поэтому
можно добавлять = fastapi.Body() а можно не добалять,
потому что обычной функции ты сразу перечисляешь в объявлении данные
котоорые будешь передавать, а тут ты передаёшь целый 
объект pydantic (по факту JSON) и fastapi оттуда достаёт данные   """
    return crud.update_user(user).to_dict() #т к просто апдейт юзера возвращает прямо базу данных, а нам нужен жсон
         


@api.delete("/user/delete{user_id}")
@db_session
def delete_user(user_id: int = fastapi.Path()):  # используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
    crud.get_user_by_id(user_id).delete()
    return True

@api.get("/user/{user_id}/wallet/get_wallet_balance")
@crud.db_session #баланс юзера по айди
def get_wallet_balance(user_id: int):
    return crud.User[user_id].wallet.balance

@api.get("/wallet/general_balance")
@crud.db_session
def get_general_balance():
    crud.update_all_wallets()
    sum: int = 0
    for i in crud.select(u.balance for u in crud.Wallet):
        sum += i

    return sum

@api.get("/users")
@crud.db_session
def  get_all_users():
    users = []
    for i in crud.select(u for u in crud.User):
        users.append(i.to_dict()) #не забывай переделывать в словарь
    return users


@api.post("/create_transaction")
@crud.db_session #получить объект юзера по его тг айди
def create_transaction(transaction: pydantic_models.Create_Transaction):
    user = crud.select(i for i in models.User if i.tg_ID == transaction.tg_id).get()

    return     crud.create_transaction(user, transaction.amount_btc_without_fee, transaction.receiver_address).to_dict()



