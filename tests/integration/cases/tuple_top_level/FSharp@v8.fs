module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FInt 1L;
    FStr "email";
    FStr "a@gmail.com";
    FInt 100L
]
