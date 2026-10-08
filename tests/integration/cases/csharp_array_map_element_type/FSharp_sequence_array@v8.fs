module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("d", [|FMap [("a", [|FMap [("b", [|FInt 1L; [|FFloat 2.5; [|FStr "x"; [|FBool true|]|]|]|])]|])]|])
]
