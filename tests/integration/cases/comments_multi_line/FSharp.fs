module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    // line 1
    // line 2
    FStr "a"
]
