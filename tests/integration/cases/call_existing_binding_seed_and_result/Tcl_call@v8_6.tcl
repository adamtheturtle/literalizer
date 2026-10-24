proc make_widget {args} {return {}}
proc consume_widget {args} {}
set my_data [make_widget 0]
consume_widget my_data
set my_data [make_widget 1]
consume_widget my_data
