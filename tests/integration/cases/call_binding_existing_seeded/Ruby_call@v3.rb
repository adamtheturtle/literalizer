def make_widget(*a); end
my_data = make_widget(count: 42)
make_widget(count: my_data)
my_data = make_widget(count: my_data)
make_widget(count: my_data)
