
import copy

from pony.orm import db_session
from requests import Request

from database import crud
import pydantic_models
import config
import fastapi
from fastapi import FastAPI, Query, Body

from database.crud import get_user_info
from pydantic_models import User_to_create

api = fastapi.FastAPI()

response = "response from server"


fake_database = {'users':[
    {
        "id":1,
        "name":"Anna",
        "nick":"Anny42",
        "balance": 15300
     },

    {
        "id":2,
        "name":"Dima",
        "nick":"dimon2319",
        "balance": 160.23
     },
    {
        "id":3,
        "name":"Vladimir",
        "nick":"Vova777",
        "balance": 200.1
     }
    ], }

""" @api.get("/")
def index():
    return response
 """

""" @api.get("/users/{user:str}")
def get_user(user):
    return {"username": user} """


@api.get("/get_user_{id:int}")
def get_user_by_id(id):
    return fake_database['users'][id-1]


@api.get('/get_info_by_user_id/{user_id:int}')
@crud.db_session
def get_info_about_user(user_id):

    return crud.get_user_info(crud.User[user_id])


@api.get('/get_user_balance_by_id/{user_id:int}')
@crud.db_session
def get_balance(user_id):
    crud.update_wallet_balance(crud.User[user_id].wallet)
    return crud.User[user_id].wallet.balance


@api.get("/get_full_info")
def get_info(limit:int = 0, random:int = 10): #любое название переменной, а снизу просто срез
    return fake_database["users"][limit:random]



'''@api.get('/')       # метод для обработки get запросов
@api.post('/')      # метод для обработки post запросов
@api.put('/')       # метод для обработки put запросов
@api.delete('/')    ''' #метод для обработки delete запросов
'''def index(requests: Request):
        return {"Requests:": [
             requests.method,
             requests.headers
        ]}
'''


@api.post("/create_user")
@crud.db_session
def creation_usera(user: User_to_create):  #смотрим чтобы входные данные соответствовали модели типов данных класса User
    crud.create_user(user.tg_ID, user.nick).to_dict()
    return True
      



@api.put('/user/{user_id}')
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