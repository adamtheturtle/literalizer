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
let my_data: Val = FMap [
    ("name", FStr "Alice");
    ("scores", FList [FInt 10L; FInt 20L; FInt 30L])
]
