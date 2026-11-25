struct Record0 { let flags: [Bool]; let values: [Double]; let ints: [Int]; let text: [String]; let nested_flags: [[Bool]]; let nested_values: [[Double]] }
let my_data = Record0(
    flags: [
        true,
        false,
    ],
    values: [
        1.5,
        -2.25,
    ],
    ints: [
        1,
        2,
    ],
    text: [
        "a",
    ],
    nested_flags: [
        [
            true,
        ],
        [
            false,
        ],
    ],
    nested_values: [
        [
            1.5,
        ],
        [
            2.25,
        ],
    ],
)
