module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let deep: Val = FList [
    FList [
        FInt 1L;
        FInt 2L
    ];
    FList [
        FInt 3L;
        FInt 4L
    ]
]
let my_data: Val = FMap [
    ("a", FMap [
        ("b", FMap [
            ("c", deep)
        ])
    ])
]
