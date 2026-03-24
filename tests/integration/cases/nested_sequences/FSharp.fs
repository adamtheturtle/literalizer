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
    FList [FList [FInt 1L; FInt 2L]; FList [FInt 3L; FInt 4L]];
    FList [FList [FInt 5L]]
]
