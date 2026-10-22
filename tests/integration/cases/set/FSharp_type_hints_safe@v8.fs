module Main

type Val =
    | FStr of string
    | FSet of Val list
let my_data: Val = FSet [
    FStr "apple";
    FStr "banana";
    FStr "cherry"
]
