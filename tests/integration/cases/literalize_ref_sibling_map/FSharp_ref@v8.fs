module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let siblingMap: Val = FMap [
    ("k", FInt 2L)
]
let my_data: Val = FList [
    FMap [("k", FInt 1L)];
    siblingMap
]
