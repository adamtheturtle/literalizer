module Main

type Val =
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [];
    FMap []
]
