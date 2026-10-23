module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FInt 1L;
    FStr "a";
    FFloat 2.5
|]
