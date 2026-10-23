module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FInt 0x2aL;
    FFloat 3.14;
    FBool true;
    FBool false;
    FStr "hello \"world\""
]
