'''
    The base item class that all others inherit.
'''


class Product():

    def __init__(self):
        """Creates a new Product.
        """

    @property
    def code(self):
        '''Gets the name of the product
        '''
        return self._code

    @code.setter
    def code(self, c):
        '''Sets the name of the product
        '''
        self._code = c

    @property
    def date(self):
        """Returns the numeric date product was acquired.
        """
        return self.acquire_date

    @date.setter
    def date(self, d):
        """Sets the acquire date in the format "MMDDYYYY"
        """
        self.acquire_date = d

    @property
    def product_code(self):
        """Returns the product code.
        """
        return self._product_code

    @product_code.setter
    def product_code(self, c):
        """Sets the product code
        """
        self._product_code = c
