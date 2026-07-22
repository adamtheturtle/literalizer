module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("replacement", FInt(-1L)); ("present", FInt 1L)];
    FMap [("replacement", FInt 2L); ("present", FInt 3L)]
]
