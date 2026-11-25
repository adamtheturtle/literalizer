module Main

type Val =
    | FList of Val list
    | FInt of int64
let my_data: Val = FList [
    FInt(-315619200L)
]
