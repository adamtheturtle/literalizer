def make_widget(Map _args) { null }
def consume(Map _args) { null }
def my_data = make_widget(count: 7)
consume(count: my_data)
my_data = make_widget(count: 13) != null ?
make_widget(count: 13) // inner
: null // trailing
consume(count: my_data)
