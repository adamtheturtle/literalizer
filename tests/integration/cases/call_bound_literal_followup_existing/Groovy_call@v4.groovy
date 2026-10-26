def make_widget(Map _args) { null }
def consume(Map _args) { null }
def my_data = make_widget(value: 42)
consume(value: my_data)
my_data = make_widget(value: 42)
consume(value: my_data)
