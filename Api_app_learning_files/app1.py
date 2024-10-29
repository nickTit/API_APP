import fastapi
import database
import config
import pydantic_models1

from fastapi import Request     # позволяет нам перехватывать запрос и получать по нему всю информацию

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


@api.get('/get_info_by_user_id/{id:int}')
def get_info_about_user(id):
    return fake_database['users'][id-1]["balance"]


@api.get("/get/real/balance")
def get_balance():
    total:float = 0
    for user in fake_database["users"]:
        total+= pydantic_models.User(**user).balance #распаковка списка user через класс User и переделывание его в JSON формат?
    return total


@api.get("/get_full_info")
def get_info(limit:int = 0, random:int = 10): #любое название переменной, а снизу просто срез
    return fake_database["users"][limit:random]



@api.get('/')       # метод для обработки get запросов
@api.post('/')      # метод для обработки post запросов
@api.put('/')       # метод для обработки put запросов
@api.delete('/')    # метод для обработки delete запросов
def index(requests: Request):
        return {"Requests:": [
             requests.method,
             requests.headers
        ]}



@api.post("/create_user")
def creation_usera(user: pydantic_models.User):  #смотрим чтобы входные данные соответствовали модели типов данных класса User
    """
Когда в пути нет никаких параметров
и не используются никакие переменные,
то fastapi, понимая, что у нас есть аргумент, который
надо заполнить, начинает искать его в теле запроса,
в данном случае он берет информацию, которую мы ему отправляем          #читай это))(
в теле запроса и сверяет её с моделью pydantic, если всё хорошо,
то в аргумент user будет загружен наш объект, который мы отправим
на сервер.
"""
    
    fake_database['users'].append(dict(user)) 
    """ если добавлять без dict() то обращаться к экземплярам класса User в функции удаления
    нужно через . то есть user.id а не user['id'], что невозможно, т.к. начальные 3
    пользователя у меня добавлены через словарь """
        
    return {'User Created!': user} 
      



@api.put('/user/{user_id}')
def update_user(id:int, user: pydantic_models.User = fastapi.Body()):
    """ 
фастапи сам понимает,
как достать данные из JSONa в теле, поэтому
можно добавлять = fastapi.Body() а можно не добалять, 
потому что обычной функции ты сразу перечисляешь в объявлении данные
котоорые будешь передавать, а тут ты передаёшь целый 
объект pydantic (по факту JSON) и fastapi оттуда достаёт данные   """

    index = 0                                    #костыль зато свой
    
   


    for user_old in fake_database["users"]:
     if id == user_old['id']:
        fake_database["users"][index] = user
        return {"Updated:" :user}
         
     index+=1
    return 0
         


@api.delete("/user/delete{user_id}")
def delete_user(user_id: int = fastapi.Path()): # используя fastapi.Path() мы явно указываем, что переменную нужно брать из пути
    for index, user in enumerate(fake_database['users']):
        if user_id == user["id"]:
            a= fake_database["users"][index]
            del fake_database["users"][index]
    return {"Deleted":a }