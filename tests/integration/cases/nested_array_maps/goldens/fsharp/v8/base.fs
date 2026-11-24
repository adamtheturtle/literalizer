module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("groups", FList [FList [FMap [("id", FInt 1L)]]; FList [FMap [("id", FInt 2L)]]])
]
