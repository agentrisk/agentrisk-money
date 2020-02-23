"""Implementation of Fowler's Money pattern"""

from __future__ import annotations
from math import floor
from babel.numbers import format_currency
from re import sub
from decimal import Decimal, ROUND_HALF_EVEN
import operator


class Money:
    """
    Money class that implements Fowler's Money pattern:
    https://martinfowler.com/eaaCatalog/money.html
    """

    def __init__(self, amount: int):
        self.__assert_amount(amount)

        self.__amount = amount
        self.__currency = "USD"

    def instance(self, amount: int) -> Money:
        """
        Return new money object using the given amount
        """

        self.__assert_amount(amount)

        return self.__class__(amount)

    def __str__(self):
        return format_currency(
            float(self.amount / 100),
            self.__currency,
            format=None,
            locale="en_US",
            currency_digits=True,
            format_type="standard")

    @staticmethod
    def from_float(amount: float) -> Money:
        """
        Return new money object instantiated from a float value
        """

        if not isinstance(amount, float):
            raise ValueError("Amount must be a float")

        return Money(floor(amount * 100))

    @staticmethod
    def from_string(currency_str: str) -> Money:
        """
        Return new money object instantiated from a string currency value
        """

        if not isinstance(currency_str, str):
            raise ValueError("Amount must be a string")

        value = Decimal(sub(r'[^\d.]', '', currency_str))
        return Money.from_float(float(value))

    @staticmethod
    def __assert_amount(amount):
        """
        Assert that given amount is an integer
        """
        if not isinstance(amount, int):
            raise ValueError("Amount must be an integer")

    @staticmethod
    def __assert_operand(operand):
        """
        Assert that given operand is a numeric type
        """
        if not isinstance(operand, (int, float)):
            raise ValueError("Operand must be a numeric value")

    @property
    def amount(self) -> int:
        """
        Return money amount
        """

        return self.__amount

    def __add__(self, other) -> Money:
        """
        Return a new money object that amounts to
        sum of this object and given money object
        """

        if isinstance(other, Money):
            return self.__class__(self.amount + other.amount)

        self.__assert_amount(other)
        return self.__class__(self.amount + other)

    def __radd__(self, other):
        """
        Return a new money object that amounts to
        sum of this object and given money object
        """

        return self.__add__(other)

    def __sub__(self, other) -> Money:
        """
        Return a new money object that amounts to
        difference of this object and given money object
        """

        if isinstance(other, Money):
            return self.__class__(self.amount - other.amount)

        self.__assert_amount(other)
        return self.__class__(self.amount - other)

    def __rsub__(self, other):
        """
        Return a new money object that amounts to
        difference of this object and given money object
        """

        return (-self).__add__(other)

    def __mul__(self, factor: (int, float)) -> Money:
        """
        Return a new money object that amounts to
        product of this object and given money object
        """

        self.__assert_operand(factor)

        return self.__class__(round(self.amount * factor))

    def __rmul__(self, factor) -> Money:
        """
        Return a new money object that amounts to
        product of this object and given money object
        """

        return self.__mul__(factor)

    def __truediv__(self, other) -> Money:
        """
        Return a new money object that amounts to
        quotient of this object and given money object
        """

        if isinstance(other, Money):
            if other.amount == 0:
                raise ZeroDivisionError()
            return round(self.amount / other.amount)

        self.__assert_operand(other)
        if other == 0:
            raise ZeroDivisionError()
        return self.__class__(round(self.amount / other))

    def __floordiv__(self, other) -> Money:
        """
        Return a new money object that amounts to
        quotient of this object and given money object
        """

        if isinstance(other, Money):
            if other.amount == 0:
                raise ZeroDivisionError()
            return self.amount // other.amount

        self.__assert_operand(other)
        if other == 0:
            raise ZeroDivisionError()
        return self.__class__(self.amount // other)

    def __eq__(self, other) -> bool:
        """
        Check if given money object value
        and currency matches this object
        """

        if isinstance(other, Money):
            return self.amount == other.amount

        self.__assert_amount(other)
        return self.amount == other

    def __gt__(self, other) -> bool:
        """
        Check if object amount is
        greater than given money amount
        """

        return self.__compare(other, operator.gt)

    def __ge__(self, other) -> bool:
        """
        Check if object amount is greater
        or if it equals to given money amount
        """

        return self.__compare(other, operator.ge)

    def __lt__(self, other) -> bool:
        """
        Check if object amount is
        less than given money amount
        """
        return self.__compare(other, operator.lt)

    def __le__(self, other) -> bool:
        """
        Check if object amount is less or
        if it equals to given money amount
        """

        return self.__compare(other, operator.le)

    def __compare(self, other, comparison_operator) -> bool:
        """
        Compare object amount to given money
        amount using the provided comparison operator
        """

        if isinstance(other, Money):
            return comparison_operator(self.amount, other.amount)

        self.__assert_amount(other)
        return comparison_operator(self.amount, other)

    def __round__(self) -> Money:
        """
        Return a new money object with a rounded amount
        """

        decimal_value = Decimal(self.amount / 100)
        quantized_value = decimal_value.quantize(exp=Decimal(1.00),
                                                 rounding=ROUND_HALF_EVEN)
        rounded = int(quantized_value)
        return self.__class__(rounded * 100)

    def __int__(self) -> int:
        """
        Return an int representation of a money object
        """

        return self.amount

    def __float__(self) -> float:
        """
        Return a float representation of a money object
        """

        return round(self.amount / 100, 2)

    def __neg__(self):
        """
        Return a new money object with a negative amount
        """

        return self.__class__(-self.amount)

    def __pos__(self):
        """
        Return a new money object with a positive amount
        """

        return self.__class__(+self.amount)

    def __abs__(self):
        """
        Return a new money object with an absolute value of the amount
        """

        return self.__class__(abs(self.amount))
