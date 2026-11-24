module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    // Configuration
    ("name", FStr "app");
    // Port setting
    ("port", FInt 3000L)
]
