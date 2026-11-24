module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0o3641100L;
    FInt(-0o2322L);
    FInt 0o377L;
    FInt(-0o12L)
]
