module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "48656c6c6f"
]
