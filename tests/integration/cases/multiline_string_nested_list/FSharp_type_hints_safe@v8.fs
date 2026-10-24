module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FStr "\nfirst line\n  indented\n\nlast line\n"]
]
