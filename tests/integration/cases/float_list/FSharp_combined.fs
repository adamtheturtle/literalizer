module Check

type Val =
    | FFloat of float
    | FList of Val list
let mutable my_data: Val = FList [
    FFloat 1.1;
    FFloat 2.2;
    FFloat 3.3
]
