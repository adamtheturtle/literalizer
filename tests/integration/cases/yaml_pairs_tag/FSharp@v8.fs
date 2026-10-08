module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("first", FInt 1L)];
    FMap [("repeated", FStr "a")];
    FMap [("repeated", FStr "b")]
]
