function make_widget() {}
let my_data = make_widget({ count: 0 });
make_widget({ count: my_data });
my_data = make_widget({ count: 1 });
make_widget({ count: my_data });
