module Main

type Val =
    | FInt of int64
    | FList of Val list
let my_data: Val array = [|
    FInt 1L;
    FInt 2L;
    FInt 3L
|]
