module Main

type Val =
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FFloat infinity;
    FFloat(-infinity);
    FFloat nan
|]
