module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [FMap [("key", FMap [("$ref", FStr "my_var")]); ("count", FInt 42L)]]
]
