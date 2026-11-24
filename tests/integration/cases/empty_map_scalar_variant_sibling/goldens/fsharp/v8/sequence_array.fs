module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
    | FMap of (string * Val) list
let my_data: Val array = [|
    FMap [("count", FInt 1L); ("name", FStr "value")];
    FMap []
|]
