module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val = FList [
    FInt 0xf4240L;
    FInt(-0x4d2L);
    FInt 0xffL;
    FInt(-0xaL)
]
