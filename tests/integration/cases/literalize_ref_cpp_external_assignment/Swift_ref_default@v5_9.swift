@discardableResult func consume_widget(_ _arg: Any = 0) -> Any { 0 }
let ref_data = [
    1,
    2,
]
let my_data = [
    0,
]
consume_widget(_arg: my_data);
my_data = ref_data
consume_widget(_arg: my_data);
