from datetime import datetime

class Offer():

    title: str
    price: float
    delivery: bool
    date: datetime.date

    def __init__(
        self, title: str, price: float, delivery: bool, date: datetime.date
    ):
        self.title = title
        self.price = price
        self.delivery = delivery
        self.date = date
    
    def offer_to_data():
        pass

    def __repr__(self):
        print(f'{self.date:12}\t{self.price:10}{self.delivery}\t{self.title}')