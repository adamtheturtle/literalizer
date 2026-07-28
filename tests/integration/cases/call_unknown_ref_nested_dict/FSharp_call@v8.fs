module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let process (_data: obj) : obj = null
let my_list: Val = FMap [
    ("unused", FStr "value")
]
process(FList [FList [FMap [("inner", my_list)]]])
