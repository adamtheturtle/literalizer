@discardableResult func process(value: Any = 0, count: Any = 0) -> Any { 0 }
let my_int: Any = 1
let my_bool: Any = true
let my_float: Any = 3.14
let my_list: Any = [
    1,
    2,
    3,
]
process(value: my_int, count: 42);
process(value: my_bool, count: 7);
process(value: my_float, count: 9);
process(value: my_list, count: 1);
