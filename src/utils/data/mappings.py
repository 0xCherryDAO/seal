from src.utils.runner import *

module_handlers = {
    'FAUCET': process_faucet,
    'ALLOWLIST_UPLOAD_FILE': process_allowlist_file_upload,
    'SUBSCRIPTION_UPLOAD_FILE': process_subscription_file_upload
}
