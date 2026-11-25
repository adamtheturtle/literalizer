my_data = {
    99999999999999999999999999: "tag",
}
# Independent native value checks.
assert all(type(key) is int for key in my_data)
assert my_data == {99999999999999999999999999: 'tag'}
