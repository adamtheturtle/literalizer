module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("numbers", FList [FInt 1L; FInt 2L]);
    ("nested", FMap [("inner", FList [FInt 3L])]);
    ("mixed", FList [FInt 4L; FStr "five"])
]
