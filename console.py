'''
    Console class defines a type of game console.
'''

from product import Product
import datetime


class Console(Product):
    def __init__(self, code, model, board, mods, a_date=datetime.datetime.now().strftime("%m%d%Y%H%M%S")):
        '''Defines a Console product.
        '''

        # Sets the console code
        self.code = code

        # Sets the acquire date. Defaults to the current date.
        self.acquire_date = a_date

        # Sets the model number of the console
        self.model = model

        # Sets the board revision
        self.board = board

        # Sets a list of mods done the the console
        self.mods = mods

        # Sets the product code for consoles
        self.product_code = f"{self.code}{self.model}{self.board}{self.acquire_date}"
