struct Record1 { let x: Int }
struct Record0 { let values: [String: [String: [String: Int]]]; let flag: Bool }
let my_data = Record0(
    values: [
        "outer": [
            "inner": Record1(
                x: 1,
            ),
        ],
    ],
    flag: true,
)
