from datetime import datetime
import requests

class Manager:
    def __init__(self, authorization: str):
        self.authorization = authorization
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0",
            "authorization": authorization
        }

    def create_portfolio(self, name: str, symbols: list() = []) -> int: 
        url = f'https://app-money.tmx.com/graphql'
        data = {"operationName":"CreateWatchlist","variables":{"name":name,"symbols":symbols},"query":"mutation CreateWatchlist($name: String, $symbols: [String]) {\n  createWatchlist(name: $name, symbols: $symbols) {\n    id\n    order\n    name\n    watchlistItems {\n      symbol\n      order\n      __typename\n    }\n    error {\n      type\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}
        result = requests.post(url, headers = self.headers, json = data).json()
        return result["data"]["createWatchlist"]["id"]

    def add_symbol(self, id: int, symbol: str):
        url = f'https://app-money.tmx.com/graphql'
        data = {"operationName":"addToWatchlist","variables":{"symbol":symbol,"watchlistId":id},"query":"mutation addToWatchlist($symbol: String!, $watchlistId: Int!) {\n  addToWatchlist(symbol: $symbol, watchlistId: $watchlistId) {\n    id\n    order\n    name\n    watchlistItems {\n      symbol\n      order\n      __typename\n    }\n    __typename\n  }\n}\n"}
        return requests.post(url, headers = self.headers, json = data)

    def add_lot(self, id: int, symbol: str, price: float, quantity: float, date: datetime = datetime.today(), fees: float = 0, skipAddSymbol: bool = False):
        if not skipAddSymbol:
            self.add_symbol(id, symbol)
        url = f'https://app-money.tmx.com/graphql'
        data = {"operationName":"createLot","variables":{"watchlistId":id,"symbol":symbol,"price":price,"shares":quantity,"fees":fees,"date":date.strftime("%x"),"notes":""},"query":"mutation createLot($watchlistId: Int!, $symbol: String!, $price: Float!, $shares: Float!, $fees: Float, $date: String!, $notes: String) {\n  createLot(watchlistId: $watchlistId, symbol: $symbol, price: $price, shares: $shares, fees: $fees, date: $date, notes: $notes) {\n    summary {\n      totalShares\n      totalLots\n      averageCost\n      averageFees\n      totalCost\n      __typename\n    }\n    lots {\n      id\n      shares\n      price\n      fees\n      date\n      notes\n      __typename\n    }\n    __typename\n  }\n}\n"}
        return requests.post(url, headers = self.headers, json = data)

    def delete_portfolio(self, id: int):
        url = f'https://app-money.tmx.com/graphql'
        data = {"operationName":"removeWatchlist","variables":{"watchlistId":id},"query":"mutation removeWatchlist($watchlistId: Int!) {\n  removeWatchlist(watchlistId: $watchlistId) {\n    id\n    order\n    name\n    __typename\n  }\n}\n"}
        return requests.post(url, headers = self.headers, json = data)

    def get_portfolios(self):
        url = f'https://app-money.tmx.com/graphql'
        data = {"operationName":"getWatchlists","variables":{},"query":"query getWatchlists {\n  getWatchlists {\n    id\n    order\n    name\n    watchlistItems {\n      symbol\n      order\n      __typename\n    }\n    __typename\n  }\n}\n"}
        return requests.post(url, headers = self.headers, json = data).json()['data']['getWatchlists']