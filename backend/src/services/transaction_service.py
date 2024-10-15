import uuid
from typing import Optional, Any, List

from src.data.dal import TransactionDAL
from src.schema import Transaction


class TransactionService:
    def __init__(self, transaction_dal: TransactionDAL) -> None:
        self.__transaction_dal = transaction_dal

    async def get_transactions(self, **params: Optional[Any]) -> Optional[List[Transaction]]:
        return await self.__transaction_dal.get_all(**params)
    
    async def get_one_transaction(self, **params: Optional[Any]) -> Optional[Transaction]:
        return await self.__transaction_dal.get_one(**params)
    
    async def add_transaction(self, **params: Optional[Any]) -> None:
        return await self.__transaction_dal.add(**params)

    async def update_transaction(self, id: uuid.UUID, **params: Optional[Any]) -> None:
        return await self.__transaction_dal.update(id=id, **params)
