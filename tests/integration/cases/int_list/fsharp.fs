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
    FInt 1L;
    FInt 2L;
    FInt 3L
]
