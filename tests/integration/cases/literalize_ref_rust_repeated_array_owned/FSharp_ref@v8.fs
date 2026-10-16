module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let shared: Val array = [|
    FMap [("value", FInt 1L)]
|]
let my_data: Val array = [|
    shared;
    shared
|]
