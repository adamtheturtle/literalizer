def make_widget(Map _args) { null }
def consume_widget(Map _args) { null }
def my_data = make_widget(count: 42)
consume_widget(count: my_data)
my_data = make_widget(count: my_data) // note
// extra
consume_widget(count: my_data)
