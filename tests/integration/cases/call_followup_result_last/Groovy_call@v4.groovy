def make_widget(Map _args) { null }
def consume(Map _args) { null }
def my_data = make_widget(first: 42, second: 3)
consume(first: 3, second: my_data)
