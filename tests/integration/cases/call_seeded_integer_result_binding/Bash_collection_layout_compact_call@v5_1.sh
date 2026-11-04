make_widget() { :; }
consume() { :; }
declare my_data="$(make_widget 42)"
consume my_data
my_data="$(make_widget 42)"
consume my_data
