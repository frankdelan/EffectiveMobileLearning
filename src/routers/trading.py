from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from schemas import (TradingDateSchema, LastPeriodTradingSchema, LastTradingSchema, TradingDealSchema,
                     SuccessResponseSchema, ErrorResponseSchema)
from services.trading import TradingService
from utils.time_utils import get_expire_time

router = APIRouter(
    prefix='/api/trading',
    tags=['Trading']
)


@router.get('/list/{count}', response_model=SuccessResponseSchema | ErrorResponseSchema)
@cache(expire=get_expire_time())
async def get_last_trading_dates(count: int,
                                 service: TradingService = Depends(TradingService)):
    dates: list[TradingDateSchema] = await service.get_last_trading_dates(count)
    if not dates:
        return ErrorResponseSchema(detail='Deals not found')
    return SuccessResponseSchema(data=dates,
                                 detail=f'last {abs(count)} trading dates')


@router.get('/list', response_model=SuccessResponseSchema | ErrorResponseSchema)
@cache(expire=get_expire_time())
async def get_trading_results(data: LastTradingSchema = Depends(LastTradingSchema),
                              service: TradingService = Depends(TradingService)):
    deals = await service.get_trading_results(data.model_dump())
    if not deals:
        return ErrorResponseSchema(detail='Deals not found')
    return SuccessResponseSchema(data=[TradingDealSchema.model_validate(item) for item in deals],
                                 detail=f'last trading dates')


@router.get('/period', response_model=SuccessResponseSchema | ErrorResponseSchema)
@cache(expire=get_expire_time())
async def get_dynamics(data: LastPeriodTradingSchema = Depends(LastPeriodTradingSchema),
                       service: TradingService = Depends(TradingService)):
    deals = await service.get_dynamics(data.model_dump())
    if not deals:
        return ErrorResponseSchema(detail='Deals not found')
    return SuccessResponseSchema(data=[TradingDealSchema.model_validate(item) for item in deals],
                                 detail=f'deals for the period from {data.start_date} to {data.end_date}')
