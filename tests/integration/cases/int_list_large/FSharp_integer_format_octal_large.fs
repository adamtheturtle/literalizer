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
    FInt 0o3641100L;
    FInt(-0o2322L);
    FInt 0o377L;
    FInt(-0o12L)
]
