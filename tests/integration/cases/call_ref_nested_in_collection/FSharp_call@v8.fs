module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_a: obj, _b: obj) : obj = null
let big_list: Val = FList [
    FStr "x"
]
process(FMap [("k", big_list)], FMap [("m", big_list)])
