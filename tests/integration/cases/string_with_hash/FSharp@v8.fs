module Main

type Val =
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FStr "issue #{42}";
    FStr "color #red"
]
