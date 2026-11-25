function make_widget() {}
function consume() {}
let my_data = make_widget({ count: null });
consume({ count: my_data });
my_data = make_widget({ count: 42 }) // note;
consume({ count: my_data });
