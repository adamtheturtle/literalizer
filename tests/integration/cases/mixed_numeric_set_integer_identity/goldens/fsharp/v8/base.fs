module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FSet of Val list
let my_data: Val = FSet [
    FFloat 1.5;
    FInt 9007199254740993L
]
