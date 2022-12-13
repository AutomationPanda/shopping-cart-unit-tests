import pytest
from orders import *
from unittest.mock import Mock


# --------------------------------------------------------------------------------
# Tests for calculate_total
# --------------------------------------------------------------------------------

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
        (-90, 10, 20, 0.05, 'subtotal'),
        (90, -10, 20, 0.05, 'shipping'),
        (90, 10, -20, 0.05, 'discount'),
        (90, 10, 20, -0.05, 'tax_percent'),
    ]
)
def test_calculate_total_negatives(subtotal, shipping, discount, tax_percent, variable):
    with pytest.raises(ValueError) as e:
        calculate_total(subtotal, shipping, discount, tax_percent)
    assert str(e.value) == f'{variable} cannot be negative'


# --------------------------------------------------------------------------------
# Tests for Item
# --------------------------------------------------------------------------------

def test_Item_init():
    item = Item('stuff', 12.34, 3)
    assert item.name == 'stuff'
    assert item.unit_price == 12.34
    assert item.quantity == 3


def test_Item_init_default_quantity():
    item = Item('stuff', 12.34)
    assert item.name == 'stuff'
    assert item.unit_price == 12.34
    assert item.quantity == 1


@pytest.mark.parametrize(
    'unit_price, quantity, expected',
    [
        (12.34, 1, 12.34),
        (12.34, 3, 37.02),
        (12.34, 0, 0),
        (0, 1, 0),
    ]
)
def test_Item_calculate_item_total(unit_price, quantity, expected):
    item = Item('stuff', unit_price, quantity)
    assert expected == item.calculate_item_total()


# --------------------------------------------------------------------------------
# Tests for Order
# --------------------------------------------------------------------------------

def test_Order_init():
    order = Order()
    assert isinstance(order.items, list)
    assert len(order.items) == 0


def test_Order_add_item_to_empty():
    order = Order()
    first_item = Item('stuff', 12.34)
    order.add_item(first_item)
    assert len(order.items) == 1
    assert order.items[0] == first_item


def test_Order_add_item_to_existing():
    order = Order()
    item0 = Item('stuff', 12.34)
    item1 = Item('more', 9.99)
    order.add_item(item0)
    order.add_item(item1)
    assert len(order.items) == 2
    assert order.items[0] == item0
    assert order.items[1] == item1


def test_Order_calculate_subtotal_for_multiple_items():
    order = Order()

    item0 = Mock()
    item0.calculate_item_total.return_value = 5
    order.add_item(item0)

    item1 = Mock()
    item1.calculate_item_total.return_value = 20
    order.add_item(item1)

    assert order.calculate_subtotal() == 25


def test_Order_calculate_order_total(mocker):
    order = Order(10, 5, 0.05)
    subtotal_mock = mocker.patch.object(
        order, 'calculate_subtotal', return_value=100)
    total_mock = mocker.patch(
        'orders.calculate_total', return_value=110.25)

    order_total = order.calculate_order_total()

    assert order_total == 110.25
    subtotal_mock.assert_called_once()
    total_mock.assert_called_once_with(100, 10, 5, 0.05)


def test_Order_get_reward_points(mocker):
    order = Order()
    subtotal_mock = mocker.patch.object(
        order, 'calculate_order_total', return_value=1000)
    assert order.get_reward_points() == 1010



# --------------------------------------------------------------------------------
# Tests for DynamicallyPricedItem
# --------------------------------------------------------------------------------

@pytest.mark.parametrize(
    'unit_price, quantity, expected',
    [
        (12.34, 1, 12.34),
        (12.34, 3, 37.02),
        (12.34, 0, 0),
        (0, 1, 0),
    ]
)
def test_DynamicallyPricedItem_calculate_item_total(
    mocker, unit_price, quantity, expected):

    item = DynamicallyPricedItem(12345, quantity)
    mocker.patch.object(item, 'get_latest_price', return_value=unit_price)
    assert expected == item.calculate_item_total()
