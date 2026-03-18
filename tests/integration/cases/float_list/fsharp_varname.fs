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
    FFloat 1.1;
    FFloat 2.2;
    FFloat 3.3
]
