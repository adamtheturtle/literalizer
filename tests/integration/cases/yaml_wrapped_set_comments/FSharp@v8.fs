module Main

type Val =
    | FInt of int64
    | FSet of Val list
let my_data: Val = FSet [
    FInt 10L;  // comment for ten
    FInt 2L  // comment for two
]
