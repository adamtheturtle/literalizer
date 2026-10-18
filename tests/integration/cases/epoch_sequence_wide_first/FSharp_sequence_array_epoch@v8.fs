module Main

type Val =
    | FList of Val array
    | FInt of int64
let my_data: Val array = [|
    FInt 2147483648L;
    FInt 0L
|]
