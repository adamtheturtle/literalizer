function make_widget() {}
function consume_widget() {}
let my_data = make_widget({ count: 0 });
consume_widget({ count: my_data });
my_data = make_widget({ count: 1 });
consume_widget({ count: my_data });
