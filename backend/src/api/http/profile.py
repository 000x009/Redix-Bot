import uuid
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from aiogram.utils.web_app import WebAppInitData

from dependency_injector.wiring import inject, Provide

from src.main.ioc import Container
from src.schema import User, Order, Transaction
from src.services import UserService, OrderService, TransactionService, ProductService
from src.api.dependencies import user_provider
from src.api.schema.order import CreateOrderDTO
from src.schema.order import OrderStatus
from src.main.config import settings

router = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)


@router.get("/", response_model=User)
@inject
async def get_user(
    user_service: UserService = Depends(Provide[Container.user_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[User]:
    user = await user_service.get_one_user(user_id=user_data.user.id)

    return user
    
    
@router.get("/orders", response_model=List[Order])
@inject
async def get_user_orders(
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Order]]:
    orders = await order_service.get_orders(user_id=user_data.user.id)

    return orders


@router.get("/orders/{order_id}", response_model=Order)
@inject
async def get_one_order(
    order_id: uuid.UUID,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Order]:
    order = await order_service.get_one_order(id=order_id)
    return order


@router.get("/transactions", response_model=List[Transaction])
@inject
async def get_user_transactions(
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[List[Transaction]]:
    transactions = await transaction_service.get_transactions(user_id=user_data.user.id, is_successful=True)
    return transactions


@router.get("/transactions/{transaction_id}", response_model=Transaction)
@inject
async def get_one_transaction(
    transaction_id: uuid.UUID,
    transaction_service: TransactionService = Depends(Provide[Container.transaction_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> Optional[Transaction]:
    transaction = await transaction_service.get_one_transaction(
        user_id=user_data.user.id,
        id=transaction_id,
    )
    return transaction


@router.post("/orders")
@inject
async def create_order(
    order_data: CreateOrderDTO,
    order_service: OrderService = Depends(Provide[Container.order_service]),
    product_service: ProductService = Depends(Provide[Container.product_service]),
    user_data: WebAppInitData = Depends(user_provider),
) -> JSONResponse:
    product = await product_service.get_one_product(id=order_data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await order_service.add_order(
        id=uuid.uuid4(),
        user_id=user_data.user.id,
        product_id=order_data.product_id,
        status=OrderStatus.PROGRESS,
        additional_data=order_data.additional_data.model_json_schema(),
        name=product.name,
        price=product.price,
    )
    return JSONResponse(status_code=201, content={"message": "Order created"})