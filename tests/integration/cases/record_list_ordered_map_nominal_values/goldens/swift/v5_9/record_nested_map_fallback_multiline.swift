struct Record1 { let x: Int }
struct Record0 { let values: [[String: Record1]]; let flag: Bool }
let my_data = Record0(
    values: [
        [
            "inner": Record1(
                x: 1,
            ),
        ],
        [
            "inner": Record1(
                x: 2,
            ),
        ],
    ],
    flag: true,
)
