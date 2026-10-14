make_widget() { :; }
declare my_data="$(make_widget 42)"
my_data="$(make_widget my_data)"
make_widget my_data
