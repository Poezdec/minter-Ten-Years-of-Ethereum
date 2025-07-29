# mass-minter-Ten-Years-of-Ethereum
![telegram-cloud-photo-size-4-5921624406776461733-y](https://github.com/user-attachments/assets/86fba236-9e2f-4c6c-9f92-a20760f4598d)


1. Рандомная комиссия и gasLimit для каждой транзакции
2. Контроль лимита base_fee для экономии газа
3. Многопоточность и задержки
4. Логирование, отслеживание успешных и ошибочных кошельков (ready.txt, error.txt)

## Как использовать:

1.	Установи зависимости:

        pip install -r requirements.txt

3.  Заполни `keys.txt` приватными ключами (по одному в строке)

4.	Настрой `config.py` (лимит газа, задержки и по желанию RPC)

5.	Запусти:

        python main.py
