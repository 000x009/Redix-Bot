import uuid
from typing import Optional, TypeAlias, List, Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update, select, exists, delete, Result

from src.schema import Transaction
from src.data.models import TransactionModel


_TransactionResult: TypeAlias = Result[tuple[TransactionModel]]


class TransactionDAL:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kwargs) -> None:
        query = insert(TransactionModel).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def update(self, id: uuid.UUID, **kwargs) -> None:
        query = update(TransactionModel).where(TransactionModel.id == id).values(**kwargs)
        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, **kwargs: Optional[Any]) -> bool:
        if kwargs:
            query = select(
                exists().where(
                    *(
                        getattr(TransactionModel, key) == value
                        for key, value in kwargs.items()
                        if hasattr(TransactionModel, key)
                    )
                )
            )
        query = select(exists(TransactionModel))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def is_column_filled(self, user_id: int, *column_names: str) -> bool:
        user_exists = await self.exists(user_id=user_id)
        if not user_exists:
            return False

        query = select(
            *(
                getattr(TransactionModel, column_name)
                for column_name in column_names
                if hasattr(TransactionModel, column_name)
            )
        ).where(TransactionModel.user_id == user_id)

        result = await self.session.execute(query)
        column_value = result.scalar_one_or_none()
        return column_value is not None

    async def _get(self, **kwargs: Optional[Any]) -> Optional[_TransactionResult]:
        exists = await self.exists(**kwargs)
        if not exists:
            return None

        if kwargs:
            query = select(TransactionModel).filter_by(**kwargs)
        else:
            query = select(TransactionModel)

        result = await self.session.execute(query)
        return result

    async def get_one(self, **kwargs: Optional[Any]) -> Optional[Transaction]:
        res = await self.session.execute(select(TransactionModel).filter_by(**kwargs))
        if res:
            db_transaction = res.scalar_one_or_none()
            return Transaction(
                id=db_transaction.id,
                user_id=db_transaction.user_id,
                type=db_transaction.type,
                cause=db_transaction.cause,
                amount=db_transaction.amount,
                time=db_transaction.time,
                payment_data=db_transaction.payment_data,
                is_successful=db_transaction.is_successful,
            )
                
    async def get_all(self, **kwargs: Optional[Any]) -> Optional[List[Transaction]]:
        res = await self._get(**kwargs)

        if res:
            db_transactions = res.scalars().all()
            return [
                Transaction(
                    id=db_transaction.id,
                    user_id=db_transaction.user_id,
                    type=db_transaction.type,
                    cause=db_transaction.cause,
                    amount=db_transaction.amount,
                    time=db_transaction.time,
                    payment_data=db_transaction.payment_data,
                    is_successful=db_transaction.is_successful,
                )
                for db_transaction in db_transactions
            ]

    async def delete(self, **kwargs) -> None:
        query = delete(TransactionModel).filter_by(**kwargs)
        await self.session.execute(query)
        await self.session.commit()
