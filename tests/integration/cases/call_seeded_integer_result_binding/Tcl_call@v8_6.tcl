proc make_widget {args} {return {}}
proc consume {args} {}
set my_data [make_widget 42]
consume my_data
set my_data [make_widget 42]
consume my_data
