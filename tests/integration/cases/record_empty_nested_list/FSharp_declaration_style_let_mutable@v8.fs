module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let mutable my_data: Val = FMap [
    ("a", FList [FList [FInt 1L; FInt 2L]; FList [FInt 3L]]);
    ("b", FList [FList []; FList [FInt 1L]])
]
