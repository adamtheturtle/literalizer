module Main

type Val =
    | FInt of int64
    | FList of Val array
let my_data: Val array = [|
    FInt 1L;
    FInt 1099511627776L
|]
