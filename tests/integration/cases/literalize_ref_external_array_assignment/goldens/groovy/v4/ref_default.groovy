def consume_widget(Map _args) { null }
def shared = [
    1,
    2,
]
def my_data = [
    0,
]
consume_widget(arg_value: my_data)
my_data = shared
consume_widget(arg_value: my_data)
