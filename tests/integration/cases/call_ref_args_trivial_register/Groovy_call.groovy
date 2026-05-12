def process(Map _args) { null }
def my_int = 1
def my_bool = true
def my_float = 3.14
def my_list = [
    1,
    2,
    3,
]
process(value: my_int, count: 42)
process(value: my_bool, count: 7)
process(value: my_float, count: 9)
process(value: my_list, count: 1)
