# This file is part of sale_cart_discount_visible module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['SaleCart']
__metaclass__ = PoolMeta


class SaleCart:
    __name__ = 'sale.cart'

    def update_prices(self):
        Product = Pool().get('product.product')

        if self.product:
            with Transaction().set_context(without_special_price=True):
                self.discount = Decimal(0)
                res = super(SaleCart, self).update_prices()
                gross_unit_price = Product.get_sale_price([self.product],
                        self.quantity or 0)[self.product.id]
                if gross_unit_price:
                    unit_price_digits = self.__class__.gross_unit_price.digits[1]
                    discount_digits = self.__class__.discount.digits[1]
                    res['gross_unit_price'] = gross_unit_price.quantize(
                        Decimal(str(10.0 ** -unit_price_digits)))
                    discount = 1 - (res['unit_price'] / res['gross_unit_price'])
                    res['discount'] = discount.quantize(
                        Decimal(str(10.0 ** -discount_digits)))
        else:
            res = super(SaleCart, self).update_prices()
        return res
