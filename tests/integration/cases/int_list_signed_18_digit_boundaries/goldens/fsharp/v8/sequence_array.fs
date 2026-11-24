module Main

type Val =
    | FInt of int64
    | FList of Val array
let my_data: Val array = [|
    FInt 999999999999999999L;
    FInt(-999999999999999999L)
|]
