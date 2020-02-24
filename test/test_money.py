from decimal import Decimal
from money import Money
import pytest


def test_init_with_int():
    m = Money(1000)
    assert m.amount == 1000


def test_init_from_float():
    m = Money.from_float(1000.0)
    assert m.amount == 100000


def test_init_from_string():
    m = Money.from_string("$6,150,593.22")
    assert m.amount == 615059322


def test_init_non_int():
    with pytest.raises(ValueError):
        Money(1000.0)

    with pytest.raises(ValueError):
        Money(Decimal(1000.0))

    with pytest.raises(ValueError):
        Money("$10.00")

    with pytest.raises(ValueError):
        m = Money(1000)
        Money(m)


def test_to_str():
    m = Money(1000)
    assert str(m) == "$10.00"

    m = Money(100000)
    assert str(m) == "$1,000.00"


def test_add():
    m = Money(1000)
    assert m + 10 == Money(1010)
    assert 500 + m == Money(1500)

    with pytest.raises(ValueError):
        m + 10.0

    with pytest.raises(ValueError):
        10.0 + m


def test_subtract():
    m = Money(1000)
    assert m - 10 == Money(990)
    assert 1500 - m == Money(500)

    with pytest.raises(ValueError):
        m - 10.0

    with pytest.raises(ValueError):
        10.0 - m


def test_multiply():
    m = Money(1000)
    assert m * 10 == Money(10000)
    assert 50 * m == Money(50000)
    assert m * 10.0 == Money(10000)
    assert 50.0 * m == Money(50000)
    assert m * 1.5 == Money(1500)
    assert m * 1.0009 == Money(1001)


def test_divide():
    m = Money(1000)
    assert m / 10 == Money(100)
    assert m / 3 == Money(333)
    assert m / Money(10) == Money(100)
    assert m / 10.0 == Money(100)
    assert m // 3 == Money(333)
    assert m // Money(3) == Money(333)

    with pytest.raises(ZeroDivisionError):
        m / 0
        m / Money(0)


def test_comparison():
    m = Money(1000)

    assert m == Money(1000)
    assert m >= Money(1000)
    assert m >= Money(999)
    assert m > Money(999)
    assert m <= Money(1000)
    assert m < Money(1001)

    assert m == 1000
    assert m >= 1000
    assert m >= 999
    assert m > 999
    assert m <= 1000
    assert m < 1001

    with pytest.raises(ValueError):
        assert m == 1000.0
        assert m >= 1000.0
        assert m >= 999.0
        assert m > 999.0
        assert m <= 1000.0
        assert m < 1001.0


def test_sign():
    pos = Money(1000)
    neg = Money(-1000)

    assert -pos == neg
    assert neg == +neg
    assert abs(pos) == pos
    assert abs(neg) == pos


def test_cast():
    m = Money(1000)

    assert int(m) == 1000
    assert float(m) == 10.0


def test_round():
    assert round(Money(1001)) == 1000
    assert round(Money(1051)) == 1100
