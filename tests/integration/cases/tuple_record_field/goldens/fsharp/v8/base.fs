module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("call", FStr "send");
    ("args", FList [FInt 1L; FStr "email"; FStr "a@gmail.com"; FInt 100L])
]
