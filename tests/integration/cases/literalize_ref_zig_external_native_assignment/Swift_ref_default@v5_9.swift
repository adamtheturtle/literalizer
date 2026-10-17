@discardableResult func consume_widget(_ _arg: Any = 0) -> Any { 0 }
let shared = [
    1,
    2,
]
var my_data = [
    0,
]
consume_widget(_arg: my_data);
my_data = shared
consume_widget(_arg: my_data);
