struct Record1 { let numbers: [Int]; let strings: [String] }
struct Record0 { let omap_value: [String: Int]; let sibling_lists: Record1; let ref_marker_present: [String] }
let my_data: Any = Record0(
    omap_value: [
        "first": 1,
    ],
    sibling_lists: Record1(
        numbers: [
            1,
            2,
        ],
        strings: [
            "x",
            "y",
        ],
    ),
    ref_marker_present: [
        "$keep",
        "z",
    ],
)
