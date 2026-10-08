module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("d", FList [FMap [("a", FList [FMap [("b", FList [FInt 1L; FList [FFloat 2.5; FList [FStr "x"; FList [FBool true]]]])]])]])
]
