module Main

type Val =
    | FNull
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("outer", FMap [("a", FInt 1L); ("b", FStr "x"); ("c", FNull)])
]
