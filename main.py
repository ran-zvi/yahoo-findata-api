from financials import get_financial_data
from config import FINANCIAL_DATA_TYPES_MAP
from fastapi import FastAPI

app = FastAPI()


@app.get('/data/{symbol}')
def get_fin_data(symbol: str, type: str):
    f_type = FINANCIAL_DATA_TYPES_MAP.get(type, type)
    if f_type not in FINANCIAL_DATA_TYPES_MAP.values():
        return {'error': f'incorrect data type: {type}'}
    return get_financial_data(symbol.upper(), type)
