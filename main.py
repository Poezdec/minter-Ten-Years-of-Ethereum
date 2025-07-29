import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor
from web3 import Web3
import os
import config

CONTRACT_ADDRESS = '0x26d85a13212433fe6a8381969c2b0db390a0b0ae'
MINT_FUNC_SELECTOR = '0x1249c58b'  # Функция mint() без параметров

KEYS_FILE = 'keys.txt'
READY_FILE = 'ready.txt'
ERROR_FILE = 'error.txt'
LOG_FILE = 'mint.log'

# ---------------- ЛОГИРОВАНИЕ ----------------
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# ---------------- ФУНКЦИИ ----------------
def load_keys(filename):
    if not os.path.exists(filename):
        return []
    with open(filename) as f:
        return [line.strip() for line in f if line.strip()]

def save_ready_key(priv_key):
    with open(READY_FILE, 'a') as f:
        f.write(priv_key + '\n')

def save_error_key(priv_key):
    with open(ERROR_FILE, 'a') as f:
        f.write(priv_key + '\n')

def get_base_fee_and_priority_fee(web3):
    try:
        fee_history = web3.eth.fee_history(1, 'latest')
        base_fee = fee_history['baseFeePerGas'][-1] / 1e9
        priority_fee = round(random.uniform(0.301, 1.002), 9)
        return base_fee, priority_fee
    except Exception as e:
        logger.error(f"Ошибка получения комиссии: {e}")
        return 2.0, round(random.uniform(0.301, 1.002), 9)

def mint_nft(private_key, web3, contract_addr, mint_selector):
    account = web3.eth.account.from_key(private_key)

    while True:
        base_fee, priority_fee = get_base_fee_and_priority_fee(web3)
        if base_fee > config.MAX_BASE_FEE_GWEI:
            logger.info(f"[{account.address}] ⛽ base_fee {base_fee:.6f} > лимит {config.MAX_BASE_FEE_GWEI}. Ждём...")
            time.sleep(15)
            continue
        break

    try:
        balance = web3.eth.get_balance(account.address)
        gas_limit = random.randint(145000, 165000)
        total_cost = gas_limit * web3.to_wei(base_fee + priority_fee, 'gwei')

        if balance < total_cost:
            logger.error(f"[{account.address}] ❌ Недостаточно средств. Баланс: {web3.from_wei(balance, 'ether')} ETH")
            save_error_key(private_key)
            return

        nonce = web3.eth.get_transaction_count(account.address, 'pending')

        tx = {
            'chainId': web3.eth.chain_id,
            'to': contract_addr,
            'data': mint_selector,
            'nonce': nonce,
            'gas': gas_limit,
            'maxFeePerGas': web3.to_wei(base_fee + priority_fee, 'gwei'),
            'maxPriorityFeePerGas': web3.to_wei(priority_fee, 'gwei'),
            'type': 2
        }

        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_url = f"https://etherscan.io/tx/{tx_hash.hex()}"
        logger.info(f"[{account.address}] ✅ Минт отправлен: {tx_url} | base: {base_fee:.3f} | tip: {priority_fee:.3f} | gas: {gas_limit}")
        save_ready_key(private_key)

    except Exception as e:
        logger.error(f"[{account.address}] ❌ Ошибка при минте: {e}")
        save_error_key(private_key)

def worker(private_key):
    start_delay = random.randint(config.START_MIN_DELAY, config.START_MAX_DELAY)
    logger.info(f"[{private_key[:6]}...] ⏳ Стартовая задержка: {start_delay} сек.")
    time.sleep(start_delay)

    web3 = Web3(Web3.HTTPProvider(config.RPC_URL))
    if not web3.is_connected():
        logger.error("❌ RPC-соединение не установлено!")
        return

    checksum_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

    mint_nft(
        private_key,
        web3,
        checksum_address,
        MINT_FUNC_SELECTOR
    )

    delay = random.randint(config.MIN_DELAY, config.MAX_DELAY)
    logger.info(f"[{private_key[:6]}...] ⏳ Задержка перед следующим минтом: {delay} сек.")
    time.sleep(delay)

def main():
    all_keys = load_keys(KEYS_FILE)
    done_keys = set(load_keys(READY_FILE))
    error_keys = set(load_keys(ERROR_FILE))
    valid_keys = [k for k in all_keys if k not in done_keys and k not in error_keys]

    if not valid_keys:
        logger.info("✅ Нет новых ключей для минта.")
        return

    logger.info(f"🔑 Загружено {len(valid_keys)} ключей для минта.")

    with ThreadPoolExecutor(max_workers=config.THREADS) as executor:
        executor.map(worker, valid_keys)

if __name__ == "__main__":
    main()
