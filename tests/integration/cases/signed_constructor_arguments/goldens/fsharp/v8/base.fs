module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FInt(-42L);
    FInt 0L;
    FInt 42L;
    FFloat(-1.25);
    FFloat 0.0;
    FFloat 1.25
]
