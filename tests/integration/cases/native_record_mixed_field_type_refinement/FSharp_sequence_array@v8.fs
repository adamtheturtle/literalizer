module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("first", FMap [("items", FList ([|FInt 1L; FMap [("value", FInt 2L)]|]))]);
    ("second", FMap [("items", FList ([|FInt 1L; FMap [("value", FStr "s")]|]))])
]
