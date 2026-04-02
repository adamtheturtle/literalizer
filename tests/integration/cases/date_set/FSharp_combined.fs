module Check

type Val =
    | FSet of Val list
    | FStr of string
    | FDate of System.DateTime
let mutable my_data: Val = FSet [
    FStr (string (System.DateOnly(2024, 1, 15)));
    FStr (string (System.DateOnly(2024, 6, 1)))
]
