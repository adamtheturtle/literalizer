module Main

type Val =
    | FInt of int64
    | FList of Val list
let mutable my_data: Val array = [|
    FInt 1L
|]
