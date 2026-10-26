def make_widget(*a); end
def consume(*a); end
my_data = make_widget(first: 42, second: 3)
consume(first: 3, second: my_data)
