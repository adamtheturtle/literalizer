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

let x: Val = FList [
    FStr "2024-01-15T12:30:00+00:00";
    FStr "2024-06-30T08:00:00+00:00";
    FStr "2024-12-25T18:45:00+00:00"
]
