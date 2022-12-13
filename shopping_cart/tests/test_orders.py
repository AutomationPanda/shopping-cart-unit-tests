import pytest
from orders import *


@pytest.mark.parametrize(
    'subtotal, shipping, discount, tax_percent, expected',
    [
        (90, 10, 20, 0.05, 84.00),
        (0, 10, 5, 0.05, 5.25),
        (90, 0, 20, 0.05, 73.50),
        (90, 10, 0, 0.05, 105.00),
        (90, 10, 20, 0, 80.00),
        (10, 5, 5, 0.0875, 10.88),
        (10, 5, 5, 0.0733, 10.73),
        (10, 10, 20, 0.05, 0.00),
        (10, 5, 20, 0.05, 0.00),
    ]
)
def test_calculate_total(subtotal, shipping, discount, tax_percent, expected):
    assert calculate_total(subtotal, shipping, discount, tax_percent) == expected


@pytest.mark.parametrize(
    'subtotal, shipping, discount, tax_percent, variable',
    [
        (-90, 10, 20, 0.05, 'subtotal'),      #A
        (90, -10, 20, 0.05, 'shipping'),      #B
        (90, 10, -20, 0.05, 'discount'),      #C
        (90, 10, 20, -0.05, 'tax_percent'),   #D
    ]
)
def test_calculate_total_negatives(subtotal, shipping, discount, tax_percent, variable):
    with pytest.raises(ValueError) as e:                             #E
        calculate_total(subtotal, shipping, discount, tax_percent)   #E
    assert str(e.value) == f'{variable} cannot be negative'
