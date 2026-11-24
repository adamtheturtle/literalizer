module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0o1L;
    FInt 0o2L;
    FInt 0o3L
]
