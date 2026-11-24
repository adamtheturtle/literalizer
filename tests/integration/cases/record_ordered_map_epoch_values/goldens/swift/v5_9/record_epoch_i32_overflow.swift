struct Record0 { let values: [String: Int]; let flag: Bool; let nested_values: [String: [String: Int]]; let list_values: [String: [Int]] }
let my_data = Record0(
    values: [
        "first": 2208988800,
    ],
    flag: true,
    nested_values: [
        "first": [
            "nested": 2208988800,
        ],
    ],
    list_values: [
        "first": [
            2208988800,
        ],
    ],
)
