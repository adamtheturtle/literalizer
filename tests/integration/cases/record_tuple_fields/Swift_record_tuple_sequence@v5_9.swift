struct Record0 { let pair: (Int, Int); let mixed: (Int, String); let triple: (Int, String, Bool); let nested: ((Int, String), (Int, Bool, Double)); let empty: (); let single: (Int); let long: (Int, Int, Int, Int) }
let my_data = Record0(
    pair: (
        1,
        2,
    ),
    mixed: (
        1,
        "text",
    ),
    triple: (
        1,
        "text",
        true,
    ),
    nested: (
        (
            1,
            "text",
        ),
        (
            2,
            false,
            3.5,
        ),
    ),
    empty: (),
    single: (
        1,
    ),
    long: (
        1,
        2,
        3,
        4,
    ),
)
