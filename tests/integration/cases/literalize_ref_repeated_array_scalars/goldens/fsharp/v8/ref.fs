module Main

type Val =
    | FInt of int64
    | FList of Val array
let shared: Val array = [|
    FInt 1L;
    FInt 2L
|]
let my_data: Val array = [|
    FList (shared);
    FList (shared)
|]
