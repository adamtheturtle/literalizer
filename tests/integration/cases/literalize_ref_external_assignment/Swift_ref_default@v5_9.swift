@discardableResult func consume_widget(arg_value: Any = 0) -> Any { 0 }
let ref_data = [
    1,
    2,
]
var my_data = [
    0,
]
consume_widget(arg_value: my_data);
my_data = ref_data
consume_widget(arg_value: my_data);
