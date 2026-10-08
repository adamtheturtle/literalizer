module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("rows", [|FMap [("x", FInt 1L); ("y", FStr "a")]; FMap [("x", FInt 2L); ("y", FStr "b")]|])
]
