struct Record0 { let value: [Int] }
let shared = Record0(
    value: [
        1,
        2,
    ],
)
let my_data = [
    shared,
    shared,
]
