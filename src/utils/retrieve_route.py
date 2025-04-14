from typing import List, Optional

from loguru import logger

from src.database.base_models.pydantic_manager import DataBaseManagerConfig
from src.database.utils.db_manager import DataBaseUtils
from src.models.route import Route, Wallet


async def get_routes(private_keys: str) -> Optional[List[Route]]:
    db_utils = DataBaseUtils(
        manager_config=DataBaseManagerConfig(
            action='working_wallets'
        )
    )
    result = await db_utils.get_uncompleted_wallets()
    if not result:
        logger.success(f'Все кошельки с данной базы данных уже отработали')
        return

    routes = []
    for wallet in result:
        for private_key in private_keys:
            if wallet.private_key.lower() == private_key.lower():
                private_key_tasks = await db_utils.get_wallet_pending_tasks(private_key)
                tasks = []
                for task in private_key_tasks:
                    tasks.append(task.task_name)
                routes.append(
                    Route(
                        tasks=tasks,
                        wallet=Wallet(
                            private_key=private_key,
                            proxy=wallet.proxy,
                        )
                    )
                )
    return routes
