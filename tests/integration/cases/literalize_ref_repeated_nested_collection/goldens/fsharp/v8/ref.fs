module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let shared: Val = FList [
    FList [FInt 1L; FInt 2L];
    FMap [("value", FInt 1L)]
]
let my_data: Val = FList [
    shared;
    shared
]
