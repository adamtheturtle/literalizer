module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val array = [|
    FMap [("a", FList ([|FInt 1L|]))];
    FMap [("a", FList ([|FInt 2L|]))]
|]
