module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("single_map", FList [FMap []]);
    ("single_list", FList [FList [FInt 1L]]);
    ("single_deep", FList [FList [FList [FInt 2L]]])
]
