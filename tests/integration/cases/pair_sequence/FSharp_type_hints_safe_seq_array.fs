module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val list
let my_data: Val array = [|
    FInt 1L;
    FStr "hello"
|]
