module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FInt 1L;
    FMap [];
    FMap [("x", FInt 2L)]
]
