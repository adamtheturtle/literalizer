struct Record0 { let numbers: [String: Int]; let words: [String: String]; let nested: [String: [Int]]; let empty: [String: Any]; let flag: Bool; let nested_maps: [String: [String: Int]]; let empty_nested_maps: [String: [String: Any]] }
let my_data = Record0(
    numbers: [
        "first": 1,
    ],
    words: [
        "first": "s",
    ],
    nested: [
        "first": [
            1,
            2,
        ],
    ],
    empty: [String: Any](),
    flag: true,
    nested_maps: [
        "first": [
            "nested": 1,
        ],
    ],
    empty_nested_maps: [
        "first": [String: Any](),
    ],
)
