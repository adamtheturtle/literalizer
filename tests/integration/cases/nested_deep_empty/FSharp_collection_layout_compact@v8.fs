module Main

type Val =
    | FList of Val list
let my_data: Val = FList [
    FList [FList []; FList []]
]
