module Check

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FSet of Val list
    | FDate of System.DateTime
    | FDatetime of System.DateTime
let my_data: Val = FList [
    FStr (string (System.DateOnly(2024, 1, 15)));
    FStr (string (System.DateOnly(2024, 2, 20)))
]
