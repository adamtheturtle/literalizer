module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let actual: Val = FInt 42L
let my_data: Val = FList [
    FMap [("$ref", FInt 1L)];
    FMap [("$ref", FNull)];
    actual
]
