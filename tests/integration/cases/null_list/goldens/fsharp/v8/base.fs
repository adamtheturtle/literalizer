module Main

type Val =
    | FNull
    | FList of Val list
let my_data: Val = FList [
    FNull;
    FNull
]
