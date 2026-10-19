module Main

type Val =
    | FNull
    | FList of Val list
let myNull: Val = FNull
let my_data: Val = FList [
    myNull;
    FNull
]
