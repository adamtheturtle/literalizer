@discardableResult func consume_widget(_ _arg: Any = 0) -> Any { 0 }
let item = [
    1,
    2,
]
let my_data = [
    1,
    2,
]
consume_widget(_arg: my_data);
my_data = item
consume_widget(_arg: my_data);
