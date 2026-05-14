module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FBool true;
    FStr "hi";
    FList [FInt 1L; FInt 2L];
    FNull
]
