module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val = FList [
    FInt 0b1L;
    FStr "email";
    FStr "a@gmail.com";
    FInt 0b1100100L
]
