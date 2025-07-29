# mass-minter-Ten-Years-of-Ethereum
![telegram-cloud-photo-size-4-5921624406776461733-y](https://github.com/user-attachments/assets/86fba236-9e2f-4c6c-9f92-a20760f4598d)

## RU

1. Рандомная комиссия и gasLimit для каждой транзакции
2. Контроль лимита base_fee для экономии газа
3. Многопоточность и задержки
4. Логирование, отслеживание успешных и ошибочных кошельков (ready.txt, error.txt)

### Как использовать:

1.	Установи зависимости:

        pip install -r requirements.txt

2.  Заполни `keys.txt` приватными ключами (по одному в строке)

3.	Настрой `config.py` (лимит газа, задержки и по желанию RPC)

4.	Запусти:

        python main.py


## ENG

1. Random fee and gasLimit for each transaction
2. Base fee limit control for gas savings
3. Multithreading and delays
4. Logging, tracking successful and failed wallets (ready.txt, error.txt)

### How to Use:

1.	Install dependencies:

        pip install -r requirements.txt

2.  Fill `keys.txt` with private keys (one per line)

3.	Configure `config.py` (gas limit, delays, and optional RPC)

4.	Run:

        python main.py
