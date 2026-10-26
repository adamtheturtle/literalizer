: make_widget ;
: consume ;
: my_data +null ;
my_data consume
: my_data 42 make_widget +int ;
my_data consume
