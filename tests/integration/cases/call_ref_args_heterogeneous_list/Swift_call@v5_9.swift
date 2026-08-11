@discardableResult func process(data: Any = 0, count: Any = 0) -> Any { 0 }
let my_ints = [
    1,
    2,
    3,
]
let my_strings = [
    "a",
    "b",
]
let my_empty = [Any]()
process(data: my_ints, count: 42);
process(data: my_strings, count: 7);
process(data: my_empty, count: 99);
