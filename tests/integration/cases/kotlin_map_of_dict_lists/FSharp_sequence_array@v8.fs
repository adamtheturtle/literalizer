module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", [|FMap [("k", FInt 1L)]|]);
    ("b", [|FMap [("k", FInt 2L)]|])
]
