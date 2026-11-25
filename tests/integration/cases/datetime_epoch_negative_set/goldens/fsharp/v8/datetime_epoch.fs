module Main

type Val =
    | FSet of Val list
    | FInt of int64
let my_data: Val = FSet [
    FInt(-1L)
]
