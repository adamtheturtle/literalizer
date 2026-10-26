module Main

type Val =
    | FInt of int64
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FList ([|FInt 1L|]);
    FList ([|FFloat 2.5|])
|]
