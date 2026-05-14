module Main

type JsonVal =
    | FFloat of float
    | FList of JsonVal list
let my_data: JsonVal = FList [
    FFloat infinity;
    FFloat(-infinity);
    FFloat nan
]
