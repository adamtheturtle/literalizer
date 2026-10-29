module Main

type Val =
    | FFloat of float
    | FList of Val list
let my_data: Val = FList [
    FFloat 5.0e-324;
    FFloat 2.2250738585072014e-308;
    FFloat 1.0e-307;
    FFloat 1.0e21;
    FFloat(-1.5e300);
    FFloat 1.7976931348623157e308;
    FFloat(-1.7976931348623157e308)
]
