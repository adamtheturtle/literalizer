my_data = (
    True,
    False,
    True,
)
# Independent native value checks.
assert all(type(value) is bool for value in my_data)
assert tuple(my_data) == (True, False, True)
