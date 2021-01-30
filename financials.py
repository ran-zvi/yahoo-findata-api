from typing import List

from bs4 import BeautifulSoup
import requests

import pandas as pd

from config import URL_TEMPLATE, COLUMN_REGEX

import re


def get_financial_data(symbol: str, name: str) -> pd.DataFrame:
    raw_data = BeautifulSoup(_get_html_data(symbol, name))
    data = _extract_data(raw_data)
    return data.to_dict()


def _get_html_data(symbol: str, name: str) -> str:
    response = requests.get(URL_TEMPLATE.format(symbol=symbol, name=name))
    return response.text


def _get_column_names(soup: BeautifulSoup) -> List[str]:
    origin = soup.find('span', text=re.compile(COLUMN_REGEX)).parent.parent
    return _get_span_data(origin)[1:]


def _get_span_data(origin):
    return [span.get_text(strip=True) for span in origin.find_all('span')]


def _extract_data(soup: BeautifulSoup) -> pd.DataFrame:
    columns = _get_column_names(soup)
    data = _get_financial_data_from_soup(soup)
    index, real_data = _split_index_from_data(data)
    return _parse_output(columns, index, real_data)


def _parse_output(columns, index, real_data):
    df = pd.DataFrame(real_data, index=index, columns=columns)
    return df.applymap(cast_to_float)


def _get_financial_data_from_soup(soup):
    fin_rows = soup.find_all('div', class_='fi-row')
    data = []
    for row in fin_rows:
        data.append(_get_financial_row_data(row))
    return data


def _get_financial_row_data(row) -> List[str]:
    title = row.find('div', class_='Va(m)').get_text(strip=True)
    data = [div.get_text(strip=True) for div in row.find_all('div', attrs={'data-test': 'fin-col'})]
    return [title, *data]


def _split_index_from_data(data):
    index = []
    real_data = []
    for d in data:
        index.append(d[0])
        real_data.append(d[1:])
    return index, real_data


def cast_to_float(x: str) -> float:
    if not x:
        return -99999
    if isinstance(x, str):
        x = x.replace(',', '')
        x = -99999 if x == '-' else x
    return float(x)
