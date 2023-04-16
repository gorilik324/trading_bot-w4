# Get currency pair with slash separator

class CurrencyPair:
    def __init__(self, base_currency: str, quote_currency: str):
        self.base_currency = base_currency
        self.quote_currency = quote_currency

    def __str__(self):
        return self.base_currency + '/' + self.quote_currency

    def __repr__(self):
        return self.base_currency + '/' + self.quote_currency

    def get_base(self) -> str:
        return self.base_currency

    def get_quote(self) -> str:
        return self.quote_currency

    def get_symbol(self) -> str:
        return self.base_currency.upper() + '/' + self.quote_currency.upper()

    def get_lowercase(self) -> str:
        return self.base_currency.lower() + self.quote_currency.lower()
