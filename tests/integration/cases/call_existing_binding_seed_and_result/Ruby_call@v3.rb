def make_widget(*a); end
def consume_widget(*a); end
my_data = make_widget(count: 0)
consume_widget(count: my_data)
my_data = make_widget(count: 1)
consume_widget(count: my_data)
