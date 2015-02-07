# -*- coding: utf-8 -*-

from decimal import Decimal, ROUND_DOWN

def natural_to_atomic_unit(natural_unit):
    N_ATOMS_PER_UNIT = 100000000
    if type(natural_unit) == float:
        return int(round(natural_unit * N_ATOMS_PER_UNIT))
    elif type(natural_unit) == Decimal:
        return int(natural_unit * N_ATOMS_PER_UNIT)
    else:
        raise TypeError("natural_to_atomic_unit accepts only float and Decimal type.")


def atomic_to_natural_unit(atomic_unit):
    N_ATOMS_PER_UNIT = 100000000
    if type(atomic_unit) == int or type(atomic_unit) == long:
        return Decimal(atomic_unit) / N_ATOMS_PER_UNIT
    else:
        raise TypeError("atomic_to_natural_unit accepts only int and long type.")


def quantize_natural_unit(natural_unit):
    return Decimal(natural_unit).quantize(
        Decimal("0.00000001"), rounding=ROUND_DOWN)


def render_natural_unit(atomic_unit, unit=False):
    natural_unit_string = u" MONA" if unit else u""
    return u"{0}{1}".format(
        atomic_to_natural_unit(atomic_unit), natural_unit_string)
