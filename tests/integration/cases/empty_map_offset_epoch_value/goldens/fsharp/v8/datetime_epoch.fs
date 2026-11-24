module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FList [
    FMap [("timestamp", FInt 2208988800L)];
    FMap []
]
