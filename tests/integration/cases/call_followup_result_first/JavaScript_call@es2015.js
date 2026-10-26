function make_widget() {}
function consume() {}
const my_data = make_widget({ first: 42, second: 3 });
consume({ first: my_data, second: 3 });
