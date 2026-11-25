module Main

type Val =
    | FInt of int64
    | FList of Val array
let arrayValue: Val array = [|
    FInt 1L;
    FInt 2L
|]
let scalarValue: Val = FInt 3L
let my_data: Val array = [|
    FList (arrayValue);
    scalarValue
|]
