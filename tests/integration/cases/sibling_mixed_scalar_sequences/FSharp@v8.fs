module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("left", FList [FInt 1L; FStr "one"]);
    ("right", FList [FInt 2L; FStr "two"])
]
