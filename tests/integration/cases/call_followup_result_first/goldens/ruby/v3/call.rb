def make_widget(*a); end
def consume(*a); end
my_data = make_widget(first: 42, second: 3)
consume(first: my_data, second: 3)
