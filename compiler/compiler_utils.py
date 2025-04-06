def generate_tokens(a, b):
    # Tokens for the equation `z = (a - b) / (a + b)`
    tokens = [
        {"value": "a", "type": "variable"},
        {"value": "-", "type": "operator"},
        {"value": "b", "type": "variable"},
        {"value": "/", "type": "operator"},
        {"value": "a", "type": "variable"},
        {"value": "+", "type": "operator"},
        {"value": "b", "type": "variable"},
    ]
    return tokens


def generate_symbol_table(a, b):
    # The symbol table holds variable names, types, and values
    symbol_table = [
        {"name": "a", "type": "int", "value": a},
        {"name": "b", "type": "int", "value": b},
        {"name": "z", "type": "int", "value": 0},  # z is also an integer variable
    ]
    return symbol_table


def generate_three_address_code(a, b):
    # Three-address code (TAC) for `z = (a - b) / (a + b)`
    tac = [
        "t1 = a - b",      # t1 stores (a - b)
        "t2 = a + b",      # t2 stores (a + b)
        "z = t1 / t2",     # z stores the result of (a - b) / (a + b)
    ]
    return tac
