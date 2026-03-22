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
    FList [FFloat 1.5; FFloat 2.5];
    FList [FFloat 3.5; FFloat 4.5]
]
