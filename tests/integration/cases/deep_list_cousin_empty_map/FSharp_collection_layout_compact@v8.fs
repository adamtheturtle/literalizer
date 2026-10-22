module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("items", FList [FMap [("inner", FMap [("x", FInt 1L)])]; FMap [("inner", FMap [])]])];
    FMap [("items", FList [FMap [("inner", FMap [("x", FInt 2L)])]; FMap [("inner", FMap [])]])]
]
