def make_widget(Map _args) { null }
def consume_widget(Map _args) { null }
def my_data = make_widget(count: 0)
consume_widget(count: my_data)
my_data = make_widget(count: 1)
consume_widget(count: my_data)
