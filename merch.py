'''
    Merch class defines an other type of merchandise
'''

from product import Product
import datetime


class Merch(Product):
    def __init__(self, name, a_date=datetime.datetime.now().strftime("%m%d%Y%H%M%S")):
        '''Defines an other type of good.
        '''

        # Sets the name of the item
        self.name = name

        # Sets the acquire date. Defaults to the current date.
        self.acquire_date = a_date

        # Sets the product code for other merchandise
        self.product_code = f"{self.name}{self.acquire_date}"
