module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FList [FMap [("$ref", FStr "repeated_var")]; FInt 1L];
    FList [FMap [("$ref", FStr "single_var")]; FInt 0L];
    FList [FMap [("$ref", FStr "repeated_var")]; FInt 8L]
]
