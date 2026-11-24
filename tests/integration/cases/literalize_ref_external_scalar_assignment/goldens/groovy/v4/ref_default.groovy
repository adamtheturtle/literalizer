def consume_widget(Map _args) { null }
def my_data = 0
def shared = 1
consume_widget(arg_value: my_data)
my_data = shared
consume_widget(arg_value: my_data)
