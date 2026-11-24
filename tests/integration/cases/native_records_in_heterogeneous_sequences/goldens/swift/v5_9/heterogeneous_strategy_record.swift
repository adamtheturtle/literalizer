struct Record1 { let k: [Bool] }
struct Record0 { let h: [Any] }
let my_data = Record0(
    h: [
        1,
        "a",
        [
            2,
            "b",
        ],
        Record1(
            k: [
                true,
            ],
        ),
    ],
)
