import sys
import bit
import bit.network
#from zmq.backend import first

sys.path.append('/home/redmi/Python_test_tasks/API_APP/')
from database.db import *

import pydantic_models

@db_session
def create_wallet(user: pydantic_models.User = None, private_key: str = None, testnet: bool = True):
    if not testnet: # проверяем не тестовый ли мы делаем кошелек
        raw_wallet = bit.Key() if not private_key else bit.Key(private_key)
        print("created in Truetnet")

    else:
        
        raw_wallet = bit.PrivateKeyTestnet() if not private_key else bit.PrivateKeyTestnet(private_key)
        print("created in testnet")

    if user:    
        wallet = Wallet(user=user, private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    else:
        wallet = Wallet(private_key=raw_wallet.to_wif(), address=raw_wallet.address)
    flush()# Сохраняем запись в базе данных
    return wallet

@db_session
def create_user(tg_id: int, nick: str = None):
    if nick:
        user = User(tg_ID = tg_id, nick = nick, create_date = datetime.now(), wallet = create_wallet())
    else:
        user = User(tg_ID = tg_id,  create_date = datetime.now(), wallet = create_wallet())
    flush()# Сохраняем запись в базе данных

    return user




@db_session
def create_transaction(sender: User, amount_btc_without_fee: float, receiver_address: str, fee: float = None, testnet: bool = True  ):
    if testnet:
        wallet_of_sender = bit.PrivateKeyTestnet(sender.wallet.private_key)
        print("created in testnet")
    else:
        wallet_of_sender = bit.Key(sender.wallet.private_key)
        print("created in Truenet")
    sender.wallet.balance = wallet_of_sender.get_balance()


    if not fee:
        fee = bit.network.fees.get_fee() * 1000 #типо пересчет на 1 кб 

    if amount_btc_without_fee + fee > float(sender.wallet.balance):
       return f"не хватает средств на балансе у {sender} ||||| {sender.wallet.balance}"

    output = [(receiver_address, amount_btc_without_fee, "satoshi")]

    print("Отправка транзакции...")
    tx_hash = wallet_of_sender.send(output, fee, absolute_fee=True)
    print(f"TX Hash: {tx_hash}")

    
    transaction = Transaction(
        sender = sender,
        sender_wallet = sender.wallet,
        sender_address = sender.wallet.address,
        receiver_address = receiver_address,
        amount_btc_with_fee = amount_btc_without_fee + fee,
        amount_btc_without_fee = amount_btc_without_fee,
        fee = fee,
        date_of_transaction = datetime.now(),
        tx_hash = tx_hash

)
    return transaction


""" with db_session:
    print(create_transaction(User[1], 123, User[2].wallet)) """

testnet_wallet = bit.PrivateKeyTestnet()
print( "sdads     ",testnet_wallet.address)





@db_session
def update_wallet_balance(wallet: pydantic_models.Wallet):
    # проверяем в не в тестовой сети ли мы
    testnet = True if wallet.private_key.startswith('c') else False
    # получаем объект из Bit, для работы с биткоинами
    bit_wallet = bit.Key(wallet.private_key) if not testnet else bit.PrivateKeyTestnet(wallet.private_key)
    # получаем баланс кошелька и присваиваем значение кошельку в нашей бд
    wallet.balance = bit_wallet.get_balance()
    return wallet
@db_session
def update_all_wallets():
    # с помощью генераторного выражения выбираем все кошельки, с помощью функции select()
    for wallet in select(w for w in Wallet): 
        # обновляем баланс кошелька
        update_wallet_balance(wallet)
        # печатаем для наглядности
        print(wallet.address, wallet.balance)
    return True

@db_session
def get_user_by_id(id: int):
    return User[id]


@db_session
def get_user_by_tg_id(tg_id: int):

    return select(i for i in User if i.tg_ID == tg_id).get().to_dict()


@db_session
def get_transaction_info(transaction: pydantic_models.Transaction):
    return {"id": transaction.id,
            "sender": transaction.sender if transaction.sender else None,
            "receiver": transaction.receiver if transaction.receiver else None,
            "sender_wallet": transaction.sender_wallet if transaction.sender_wallet else None,
            "receiver_wallet": transaction.receiver_wallet if transaction.receiver_wallet else None,
            "sender_address": transaction.sender_address,
            "receiver_address": transaction.receiver_address,
            "amount_btc_with_fee": transaction.amount_btc_with_fee,
            "amount_btc_without_fee": transaction.amount_btc_without_fee,
            "fee": transaction.fee,
            "date_of_transaction": transaction.date_of_transaction,
            "tx_hash": transaction.tx_hash}


@db_session
def get_wallet_info(wallet: pydantic_models.Wallet):
    wallet = update_wallet_balance(wallet)
    return {"id": wallet.id if wallet.id else None,
            "user": wallet.user if wallet.user else None,
            "balance": wallet.balance if wallet.balance else 0.0,
            "private_key": wallet.private_key if wallet.private_key else None,
            "address": wallet.address if wallet.address else None,
            "sended_transactions": wallet.sended_transactions if wallet.sended_transactions else [],
            "received_transactions": wallet.received_transactions if wallet.received_transactions else []}


@db_session
def get_user_info(user: pydantic_models.User):
    return {"id": user.id,
            "tg_ID": user.tg_ID if user.tg_ID else None,
            "nick": user.nick if user.nick else None,
            "create_date": user.create_date,
            # получаем все данные по кошельку
            "wallet": get_wallet_info(user.wallet),
            "sended_transactions": user.sended_transactions if user.sended_transactions else [],
            "received_transactions": user.received_transactions if user.received_transactions else []}


@db_session
def update_user(user: pydantic_models.User_to_update):
    user_to_update = User[user.id]
    if user.tg_ID:
        user_to_update.tg_ID = user.tg_ID
    if user.nick:
        user_to_update.nick = user.nick
    if user.create_date:
        user_to_update.create_date = user.create_date
    if user.wallet:
        user_to_update.wallet = user.wallet
    return user_to_update