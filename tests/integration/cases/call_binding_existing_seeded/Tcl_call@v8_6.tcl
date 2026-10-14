proc make_widget {args} {return {}}
set my_data [make_widget 42]
set my_data [make_widget my_data]
make_widget my_data
