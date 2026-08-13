module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FInt of int64
let my_data: Val = FMap [
    ("ts", FInt 32535215999L)
]
