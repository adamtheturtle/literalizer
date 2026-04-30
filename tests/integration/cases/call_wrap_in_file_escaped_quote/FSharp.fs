module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FList [FStr "a\"b"]
]
