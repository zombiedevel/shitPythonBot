from typing import Dict, Any

import requests

Symbols = Dict[str, Any]

host = 'https://min-api.cryptocompare.com'


def Convert(currency: float, count: float) -> float:
    return float(currency * count)


def getCurrency(from_sym: str, to_sym: str) -> float:
    response = requests.get(f"{host}/data/price?fsym={from_sym}&tsyms={to_sym}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(str(e))

    obj = response.json()
    return obj[to_sym]


def getTopSymbols(sym: str, limit: int = 10) -> Symbols:
    response = requests.get(f"{host}/data/top/totalvolfull?limit={limit}&tsym={sym}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(str(e))
    obj = response.json()
    return {"Data": obj["Data"]}
