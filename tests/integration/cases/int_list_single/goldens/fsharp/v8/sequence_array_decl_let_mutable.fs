module Main

type Val =
    | FInt of int64
    | FList of Val array
let mutable my_data: Val array = [|
    FInt 1L
|]
