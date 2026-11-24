module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 5.0e-324;
    FFloat(-5.0e-324);
    FFloat 1.0e-310
]
