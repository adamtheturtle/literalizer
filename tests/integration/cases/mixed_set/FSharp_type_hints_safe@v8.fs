module Main

type Val =
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FSet of Val list
let my_data: Val = FSet [
    FBool true;
    FInt 42L;
    FStr "apple"
]
