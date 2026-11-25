def consume_widget(Map _args) { null }
def item = [
    1,
    2,
]
def my_data = [
    1,
    2,
]
consume_widget(arg_value: my_data)
my_data = item
consume_widget(arg_value: my_data)
