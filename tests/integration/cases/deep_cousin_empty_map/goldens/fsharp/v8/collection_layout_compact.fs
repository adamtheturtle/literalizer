module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("outer", FMap [("inner", FMap [("x", FInt 1L)])])];
    FMap [("outer", FMap [("inner", FMap [])])]
]
