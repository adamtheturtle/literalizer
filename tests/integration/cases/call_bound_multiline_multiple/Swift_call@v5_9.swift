@discardableResult func f(value: Any = 0) -> Any { 0 }
let ref_data = [
    1,
    2,
]
f(value: [
    ref_data,
]);
f(value: [
    ref_data,
]);
