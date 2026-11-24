module Main

type Val =
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FFloat 1.0e-09;
    FFloat(-1.0e-09)
|]
