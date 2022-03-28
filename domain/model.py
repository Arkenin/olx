from datetime import datetime

class Offer():

    title: str
    price: float
    delivery: bool
    date: datetime.date

    def __init__(
        self, title: str, delivery: bool = False, price: float = 0, date: datetime.date = None,
    ):
        self._title = title
        self._price = price
        self.delivery = delivery
        self.date = date
    
    def __repr__(self):
        return f'{self.date:12}\t{self.price:10}{self.delivery}\t{self.title}'

    def __hash__(self):
        return hash((self.title, self.price))
    
    def __eq__(self, other):
        if not isinstance(other, Offer):
            return False
        return other.title == self.title and other.price == self.price

    @property
    def title(self):
        return self._title

    @property
    def price(self):
        return self._price

    def _members(self):
        members = [attr for attr in dir(type(self)) if not callable(getattr(Offer, attr)) and not attr.startswith("__")]
        return members

    def offer_to_data(self):
        return {f'{item}': self.__getattribute__(item) for item in self._members()}
