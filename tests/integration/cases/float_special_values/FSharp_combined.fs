module Check

type Val =
    | FFloat of float
    | FList of Val list
let mutable my_data: Val = FList [
    FFloat infinity;
    FFloat(-infinity);
    FFloat nan
]
