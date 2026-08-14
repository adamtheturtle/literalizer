module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let deep: Val = FList [
    FList [
        FStr "one";
        FStr "two"
    ];
    FList [
        FStr "three";
        FStr "four"
    ]
]
let my_data: Val = FMap [
    ("a", FMap [
        ("b", FMap [
            ("c", deep)
        ])
    ])
]
