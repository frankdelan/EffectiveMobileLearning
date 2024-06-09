from fastapi import FastAPI
from routers.trading import router as trading_router

app = FastAPI()


app.include_router(trading_router)

