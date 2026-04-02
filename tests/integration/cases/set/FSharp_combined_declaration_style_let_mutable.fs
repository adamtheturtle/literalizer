module Check

type Val =
    | FStr of string
    | FSet of Val list
let mutable my_data: Val = FSet [
    FStr "apple";
    FStr "banana";
    FStr "cherry"
]
