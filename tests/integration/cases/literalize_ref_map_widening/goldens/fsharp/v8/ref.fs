module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let stringMap: Val = FMap [
    ("k", FStr "s")
]
let my_data: Val = FList [
    stringMap;
    FMap [("k", FInt 1L)]
]
