struct Record0 { let numbers: (Int, Int); let nested_numbers: ((Int, Int), (Int, Int)); let words: (String); let flag: Bool }
let my_data = Record0(
    numbers: (
        1,
        2,
    ),
    nested_numbers: (
        (
            3,
            4,
        ),
        (
            5,
            6,
        ),
    ),
    words: (
        "s",
    ),
    flag: true,
)
