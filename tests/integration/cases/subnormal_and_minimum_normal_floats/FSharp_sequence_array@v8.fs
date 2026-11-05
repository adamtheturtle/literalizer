module Main

type Val =
    | FFloat of float
    | FList of Val array
let my_data: Val array = [|
    FFloat 5.0e-324;
    FFloat(-5.0e-324);
    FFloat 2.2250738585072014e-308
|]
