module Main

type Val =
    | FSet of Val list
    | FInt of int64
let my_data: Val = FSet [
    FInt(-2147483649L);
    FInt(-2147483648L);
    FInt 2147483647L;
    FInt 2147483648L
]
