struct Record0 { let flags: (Bool, Bool); let values: (Double, Double); let ints: (Int, Int); let text: (String); let nested_flags: ((Bool), (Bool)); let nested_values: ((Double), (Double)) }
let my_data = Record0(
    flags: (
        true,
        false,
    ),
    values: (
        1.5,
        -2.25,
    ),
    ints: (
        1,
        2,
    ),
    text: (
        "a",
    ),
    nested_flags: (
        (
            true,
        ),
        (
            false,
        ),
    ),
    nested_values: (
        (
            1.5,
        ),
        (
            2.25,
        ),
    ),
)
