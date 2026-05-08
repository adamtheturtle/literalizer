def process(Map _args) { null }
def my_ints = [
    1,
    2,
    3,
]
def my_strings = [
    "a",
    "b",
]
process(data: my_ints, count: 42)
process(data: my_strings, count: 7)
