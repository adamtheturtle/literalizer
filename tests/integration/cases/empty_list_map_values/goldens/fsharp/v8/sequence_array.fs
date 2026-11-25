module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FList ([|FInt 1L|]));
    ("b", FList ([||]))
]
