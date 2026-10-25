@discardableResult func consume_widget(arg_value: Any = 0) -> Any { 0 }
let item = [
    1,
    2,
]
var my_data = [
    1,
    2,
]
consume_widget(arg_value: my_data);
my_data = item
consume_widget(arg_value: my_data);
