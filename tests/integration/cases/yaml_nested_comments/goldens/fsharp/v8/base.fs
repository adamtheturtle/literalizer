module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FMap [
        // inner note
        ("b", FInt 1L)  // inline b
    ]);
    ("list", FList [
        FInt 1L;  // first
        FInt 2L  // second
    ])
]
