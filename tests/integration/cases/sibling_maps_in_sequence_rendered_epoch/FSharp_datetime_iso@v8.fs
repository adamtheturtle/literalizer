module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("k", FStr "2040-01-01T00:00:00+00:00")];
    FMap [("k", FInt 1L)]
]
