module Main

type Val =
    | FInt of int64
    | FSet of Val list
let my_data: Val = FSet [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
