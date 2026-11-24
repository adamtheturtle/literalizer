module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FInt(-0x2aL);
    FInt 0x0L;
    FInt 0x2aL;
    FFloat(-1.25);
    FFloat 0.0;
    FFloat 1.25
]
