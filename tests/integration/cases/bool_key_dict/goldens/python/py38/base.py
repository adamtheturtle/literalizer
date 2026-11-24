my_data = {
    True: "yes",
    False: "no",
}
# Independent native value checks.
assert all(type(key) is bool for key in my_data)
assert my_data == {True: 'yes', False: 'no'}
