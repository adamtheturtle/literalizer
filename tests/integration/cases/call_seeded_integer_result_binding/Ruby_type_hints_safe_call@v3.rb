def make_widget(*a); end
def consume(*a); end
my_data = make_widget(count: 42)
consume(count: my_data)
my_data = make_widget(count: 42)
consume(count: my_data)
