my_data = (
    True,
    False,
    True,
)
# Independent native value checks.
assert isinstance(my_data, (list, tuple))
assert all(type(value) is bool for value in my_data)
assert tuple(my_data) == (True, False, True)
