def calculate_total(subtotal, shipping, discount, tax_percent):
    if subtotal < 0:
        raise ValueError('subtotal cannot be negative')
    if shipping < 0:
        raise ValueError('shipping cannot be negative')
    if discount < 0:
        raise ValueError('discount cannot be negative')
    if tax_percent < 0:
        raise ValueError('tax_percent cannot be negative')

    amount = subtotal + shipping - discount
    if amount < 0:
        total = 0
    else:
        total = amount * (1 + tax_percent)

    rounded = round(total, 2)
    return rounded
