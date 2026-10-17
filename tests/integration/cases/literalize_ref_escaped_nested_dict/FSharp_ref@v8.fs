module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let existing: Val = FInt 1L
let my_data: Val = FMap [
    ("nested", FList [FInt 0L; existing])
]
