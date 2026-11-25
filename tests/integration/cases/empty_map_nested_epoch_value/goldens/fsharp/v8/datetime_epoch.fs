module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FList [
    FMap [("nested", FMap [("times", FList [FInt(-2208988800L)])])];
    FMap []
]
