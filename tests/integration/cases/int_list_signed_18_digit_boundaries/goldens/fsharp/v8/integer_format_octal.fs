module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0o67405553164730777777L;
    FInt(-0o67405553164730777777L)
]
