: make_widget ;
: my_data 42 make_widget +int ;
my_data make_widget
: my_data my_data make_widget ;
my_data make_widget
