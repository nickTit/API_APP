import requests



'''try:
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Транзакция успешно отправлена!")
        print(response.json())
    else:
        print(f"Ошибка: {response.status_code} - {response.json().get('error')}")
except requests.RequestException as e:
    print(f"Ошибка при подключении к BlockCypher API: {e}")
'''

address = "mqKf6GdfMfZHoWSbiQ8wTF7GNPQd1xfKJ8"
url = f"https://api.blockcypher.com/v1/btc/test3/addrs/{address}?unspentOnly=true"

response = requests.get(url)
if response.status_code == 200:
    print("UTXO для адреса:")
    print(response.json())
else:
    print(f"Ошибка: {response.status_code} - {response.json().get('error')}")
