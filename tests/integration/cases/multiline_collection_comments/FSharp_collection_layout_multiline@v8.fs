module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FList [
        FInt 1L;
        FInt 2L;
        FInt 3L
    ]);  // inline a
    ("b", FInt 2L)  // inline b
]
