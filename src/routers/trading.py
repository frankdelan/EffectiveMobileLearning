from typing import Union, Optional

from fastapi import APIRouter, Depends, HTTPException

from schemas import TradingDateSchema, LastPeriodTradingSchema, LastTradingSchema, TradingDealSchema
from schemas.wrapper import SuccessResponseSchema
from services.trading import TradingService

router = APIRouter(
    prefix='/api/trading',
    tags=['Trading']
)


@router.get('/dates/{count}', response_model=SuccessResponseSchema)
async def get_last_trading_dates(count: int,
                                 service: TradingService = Depends(TradingService)):
    dates: list[TradingDateSchema] = await service.get_last_trading_dates(count)
    if not dates:
        raise HTTPException(status_code=404, detail='Deals not found')
    return SuccessResponseSchema(data=dates, detail=f'last {count} trading dates')


@router.get('/list')
async def get_trading_results(data: LastTradingSchema = Depends(LastTradingSchema),
                              service: TradingService = Depends(TradingService)):
    deals = await service.get_trading_results(data.model_dump())
    ready_deals: list[TradingDealSchema] = [TradingDealSchema.model_validate(item) for item in deals]
    if not deals:
        raise HTTPException(status_code=404, detail='Deals not found')
    return SuccessResponseSchema(data=ready_deals, detail=f'last trading dates')


@router.get('/dynamics')
async def get_dynamics(data: LastPeriodTradingSchema = Depends(LastPeriodTradingSchema),
                       service: TradingService = Depends(TradingService)):
    deals = await service.get_dynamics(data.model_dump())
    ready_deals: list[TradingDealSchema] = [TradingDealSchema.model_validate(item) for item in deals]
    if not deals:
        raise HTTPException(status_code=404, detail='Deals not found')
    return SuccessResponseSchema(data=ready_deals, detail=None)


