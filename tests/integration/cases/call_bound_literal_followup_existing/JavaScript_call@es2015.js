function make_widget() {}
function consume() {}
let my_data = make_widget({ value: 42 });
consume({ value: my_data });
my_data = make_widget({ value: 42 });
consume({ value: my_data });
