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

let my_data: Val = FMap [
    ("date", FStr (string (System.DateOnly(2024, 1, 15))));
    ("datetime", FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0))))
]
