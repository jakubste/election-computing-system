from decimal import Decimal


def ell_p_norm(values, p):
    """
    Returns ell_p norm of values

    :type values: list of int
    :type p: int
    :rtype: Decimal
    """
    values = [x ** p for x in values]
    value = reduce(lambda x, y: x + y, values)
    value = Decimal(value) ** Decimal(1.0 / p)
    return value
