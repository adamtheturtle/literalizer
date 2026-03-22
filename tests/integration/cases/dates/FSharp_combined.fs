type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
    | FSet of Val list
module Check

let my_data: Val = FMap [
    ("date", FStr "2024-01-15");
    ("datetime", FStr "2024-01-15T12:30:00+00:00")
]
