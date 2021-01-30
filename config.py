URL_TEMPLATE = "https://finance.yahoo.com/quote/{symbol}/{name}?p={symbol}"

FINANCIAL_DATA_TYPES_MAP = {
    'f': 'financials',
    'cf': 'cash-flow',
    'bs': 'balance-sheet'
}

COLUMN_REGEX = "^Breakdown"
