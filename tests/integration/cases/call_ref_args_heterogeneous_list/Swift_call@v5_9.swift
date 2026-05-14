@discardableResult func process(data: Any = 0, count: Any = 0) -> Any { 0 }
let my_ints: Any = [
    1,
    2,
    3,
]
let my_strings: Any = [
    "a",
    "b",
]
let my_empty: Any = [Any]()
process(data: my_ints, count: 42);
process(data: my_strings, count: 7);
process(data: my_empty, count: 99);
