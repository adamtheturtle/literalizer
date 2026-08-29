module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_a: obj) : obj = null
let big_list: Val = FList [
    FStr "x"
]
process(FMap [("m", big_list)])
