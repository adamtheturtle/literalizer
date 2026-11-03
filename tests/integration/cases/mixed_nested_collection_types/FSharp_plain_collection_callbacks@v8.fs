module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("lists", FList [FList [FInt 1L]; FList [FStr "x"]; FList []]);
    ("maps", FList [FMap [("x", FInt 1L)]; FMap [("x", FStr "s")]]);
    ("empties", FMap [("a", FList [FInt 1L]); ("b", FList [])])
]
