module Main

type Val =
    | FInt of int64
    | FStr of string
    | FList of Val array
let my_data: Val array = [|
    FList ([|FInt 1L; FStr "two"|]);
    FList ([||])
|]
