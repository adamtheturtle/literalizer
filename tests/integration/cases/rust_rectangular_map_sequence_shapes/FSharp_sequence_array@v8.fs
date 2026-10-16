module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", [|FMap [("item", [|FInt 1L|])]|]);
    ("b", [|FMap [("item", [|FInt 2L|])]|])
]
