module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable my_data: Val = FList [
    FInt 1L;
    FInt 2L;
    FInt 3L
]
