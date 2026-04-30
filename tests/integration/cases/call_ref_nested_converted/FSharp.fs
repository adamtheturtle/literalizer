module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [FList [FMap [("$ref", FStr "myVar")]; FInt 42L; FStr "static"]]
]
