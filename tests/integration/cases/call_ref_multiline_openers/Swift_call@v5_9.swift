@discardableResult func consume(items: Any = 0, mapping: Any = 0) -> Any { 0 }
let foo = 42
consume(items: [
    [
        "other": 1,
    ],
    foo,
], mapping: [
    "left": foo,
    "other": 1,
]);
