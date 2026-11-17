my_data = (
    9223372036854775807,
    9223372036854775808,
)
# Independent native value checks.
assert all(type(value) is int for value in my_data)
assert tuple(my_data) == (9223372036854775807, 9223372036854775808)
