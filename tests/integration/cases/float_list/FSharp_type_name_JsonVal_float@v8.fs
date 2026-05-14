module Main

type JsonVal =
    | FFloat of float
    | FList of JsonVal list
let my_data: JsonVal = FList [
    FFloat 1.1;
    FFloat(-2.2);
    FFloat 3.3
]
