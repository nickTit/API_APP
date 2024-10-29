from pony.orm import *

db = Database()


class User(db.Entity):
    user_id = Required(str)
    nick = Required(str)
    age = Required(int) 
    wallets = Set('Wallet')


class Wallet(db.Entity):
    address = Required(str)
    private_key = Required(str)
    owner = Required(User)


try:
    db.bind(provider='sqlite', filename='/home/redmi/Python_test_tasks/API_APP/database/database.sqlite', create_db=True)
except Exception as Ex:
    print(Ex)

set_sql_debug()

db.generate_mapping(create_tables=True) #непосредственно создание самих дб, т.к. до этого по факту было только объявление макета

@db_session
def print_user_name(user_id):
    u = User[user_id]
    print(u.nick)
    # кэш сессии базы данных будет очищен автоматически
    # соединение с базой данных будет возвращено в пул

@db_session
def add_wallet(user_id, address, private_key):
    Wallet(address=address, private_key=private_key, owner=User[user_id])
    # commit() будет выполнен автоматически
    # кэш сессии базы данных будет очищен автоматически
    # соединение с базой данных будет возвращено в пул
"""with db_session:
    u1 = User(nick='John', user_id="20", age=25)
    u2 = User(nick='Mary', user_id="22", age=26)
    u3 = User(nick='Bob', user_id="30", age=35)
    w1 = Wallet(address='address1', private_key='private_key1', owner=u2)
    w2 = Wallet(address='address2', private_key='private_key2', owner=u3)
"""