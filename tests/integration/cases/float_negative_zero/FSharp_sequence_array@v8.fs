module Main

type Val =
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FFloat(-0.0);
    FFloat 1.5
|]
