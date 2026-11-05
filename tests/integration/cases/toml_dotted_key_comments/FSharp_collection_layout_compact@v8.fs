module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // first dotted key
    // second dotted key
    ("a", FMap [("b", FInt 1L); ("c", FInt 2L)])
]
