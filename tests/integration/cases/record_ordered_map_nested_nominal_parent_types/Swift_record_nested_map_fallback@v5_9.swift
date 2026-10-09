struct Record2 { let x: Int }
struct Record1 { let values: [String: [String: Record2]]; let flag: Bool }
struct Record4 { let y: String }
struct Record3 { let values: [String: [String: Record4]]; let flag: Bool }
struct Record0 { let first: Record1; let second: Record3 }
let my_data = Record0(
    first: Record1(
        values: [
            "outer": [
                "inner": Record2(
                    x: 1,
                ),
            ],
        ],
        flag: true,
    ),
    second: Record3(
        values: [
            "outer": [
                "inner": Record4(
                    y: "s",
                ),
            ],
        ],
        flag: false,
    ),
)
