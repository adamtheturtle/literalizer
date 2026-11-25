module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [FMap [("value", FInt 1L)]];
    FList [FMap [("value", FInt 1099511627776L)]]
]
