module Main

type Val =
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("outer", FList [FList [FStr "nested first line\n  indented\n\nnested last line\n"]])
]
