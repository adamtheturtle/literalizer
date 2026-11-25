module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("k", FInt 2208988800L)];
    FMap [("k", FInt 1L)]
]
