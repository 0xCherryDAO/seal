MOBILE_PROXY = False
ROTATE_IP = False

SHUFFLE_WALLETS = False

TG_BOT_TOKEN = ''  # str ('2282282282:AAZYB35L2PoziKsri6RFPOASdkal-z1Wi_s')
TG_USER_ID = None  # int (22822822) or None

SUI_TESTNET_RPC = 'https://fullnode.testnet.sui.io:443'
CAPSOLVER_API = 'CAP-...'  # https://dashboard.capsolver.com/

RETRIES = 3  # Сколько раз повторять 'зафейленное' действие
PAUSE_BETWEEN_RETRIES = 15  # Пауза между повторами

PAUSE_BETWEEN_WALLETS = [10, 20]
PAUSE_BETWEEN_MODULES = [10, 20]

FAUCET = False
ALLOWLIST_UPLOAD_FILE = False  # Allowlist Example
SUBSCRIPTION_UPLOAD_FILE = False  # Subscription Example


class UploadSettings:
    number_of_uploads = [2, 2]  # Сколько загрузок делать
    create_new_entry = True  # Создавать ли новый entry
