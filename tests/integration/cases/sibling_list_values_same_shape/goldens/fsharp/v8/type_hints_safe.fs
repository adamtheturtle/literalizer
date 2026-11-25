module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("test", FList [FInt 5L; FList [FStr "compile"; FStr "test"]]);
    ("package", FList [FInt 7L; FList [FStr "link"; FStr "test"]])
]
