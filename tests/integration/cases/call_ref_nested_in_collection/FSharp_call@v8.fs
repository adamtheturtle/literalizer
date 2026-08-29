module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_a: obj, _b: obj) : obj = null
let big_list: Val = FList [
    FStr "x"
]
process(FMap [("k", big_list)], FInt 2L)
