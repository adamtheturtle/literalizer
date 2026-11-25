module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("a", FList ([|FMap [("item", FList ([|FInt 1L|]))]|]));
    ("b", FList ([|FMap [("item", FList ([|FInt 2L; FInt 3L|]))]|]))
]
