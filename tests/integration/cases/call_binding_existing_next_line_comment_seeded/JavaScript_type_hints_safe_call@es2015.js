function make_widget() {}
function consume_widget() {}
let my_data = make_widget({ count: 42 });
consume_widget({ count: my_data });
my_data = make_widget({ count: my_data })
// note;
consume_widget({ count: my_data });
