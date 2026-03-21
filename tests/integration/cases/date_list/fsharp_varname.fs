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

let my_data: Val = FList [
    FStr "2024-01-15";
    FStr "2024-06-30";
    FStr "2024-12-25"
]
