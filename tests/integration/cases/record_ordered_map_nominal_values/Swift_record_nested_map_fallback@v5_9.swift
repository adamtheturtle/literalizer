struct Record1 { let x: Int }
struct Record0 { let values: [String: [String: Int]]; let flag: Bool }
let my_data = Record0(
    values: [
        "first": Record1(
            x: 1,
        ),
        "second": Record1(
            x: 2,
        ),
    ],
    flag: true,
)
