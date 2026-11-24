my_data = {
    1: "one",
    2: "two",
    42: "answer",
}
# Independent native value checks.
assert all(type(key) is int for key in my_data)
assert my_data == {1: 'one', 2: 'two', 42: 'answer'}
