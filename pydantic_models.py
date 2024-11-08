from datetime import datetime
import pydantic

class User(pydantic.BaseModel):
    id: int
    tg_ID: int
    nick: str = None
    create_date: datetime
    wallet: 'Wallet'
    sended_transactions: list['Transaction'] = []
    received_transactions: list['Transaction'] = []


class Transaction(pydantic.BaseModel):
    id: int
    sender: User = None
    receiver: User= None
    sender_wallet: 'Wallet'
    receiver_wallet: 'Wallet'
    sender_address: str = None
    receiver_address: str = None
    amount_btc_with_fee: float
    amount_btc_without_fee: float
    fee: float
    date_of_transaction: datetime
    tx_hash : str

class Wallet(pydantic.BaseModel):
    id: int
    user: User = None
    balance: float = 0.0
    private_key: str
    address: str
    sended_transactions: list[Transaction] = []
    received_transactions:list[Transaction] = []


class User_to_update(pydantic.BaseModel):
    id: int
    tg_ID:  int =None
    nick:   str = None
    create_date: datetime = None
    wallet: Wallet = None

class User_to_create(pydantic.BaseModel):
    tg_ID:  int = None
    nick:   str = None


class Create_Transaction(pydantic.BaseModel):
    tg_id: str
    receiver_address: str
    amount_btc_without_fee: float


    
