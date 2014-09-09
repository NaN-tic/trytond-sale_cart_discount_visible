#This file is part of sale_cart_discount_visible module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.config import CONFIG
DISCOUNT_DIGITS = int(CONFIG.get('discount_digits', 4))

__all__ = ['SaleCart']
__metaclass__ = PoolMeta


class SaleCart:
    __name__ = 'sale.cart'

    def update_prices(self):
        if hasattr(self, 'product'):
            self.discount = Decimal(0)
            res = super(SaleCart, self).update_prices()
            if self.gross_unit_price and self.unit_price:
                discount = 1 - (self.unit_price / self.gross_unit_price)
                res['discount'] = discount.quantize(
                    Decimal(str(10.0 ** -DISCOUNT_DIGITS)))
        else:
            res = super(SaleCart, self).update_prices()
        return res
