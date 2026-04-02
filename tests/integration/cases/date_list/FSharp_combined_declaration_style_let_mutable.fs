module Check

type Val =
    | FList of Val list
    | FStr of string
    | FDate of System.DateTime
let mutable my_data: Val = FList [
    FStr (string (System.DateOnly(2024, 1, 15)));
    FStr (string (System.DateOnly(2024, 2, 20)))
]
