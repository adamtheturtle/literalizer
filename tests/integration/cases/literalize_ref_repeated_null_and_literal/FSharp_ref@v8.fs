module Main

type Val =
    | FNull
    | FList of Val list
let value: Val = FNull
let my_data: Val = FList [
    value;
    value;
    FNull
]
