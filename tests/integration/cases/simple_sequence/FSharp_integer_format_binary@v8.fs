module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FInt 0b1L;
    FStr "hello";
    FBool true;
    FNull
]
