def make_widget(Map _args) { null }
def consume(Map _args) { null }
def my_data = make_widget(count: 42)
consume(count: my_data)
my_data = make_widget(count: 42)
consume(count: my_data)
