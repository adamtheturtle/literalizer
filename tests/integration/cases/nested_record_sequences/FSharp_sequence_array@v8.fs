module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val array = [|
    FList ([|FMap [("a", FInt 1L)]|]);
    FList ([|FMap [("a", FInt 2L)]|])
|]
