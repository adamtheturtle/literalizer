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
    // Configuration
    ("name", FStr "app");
    // Port setting
    ("port", FInt 3000L)
]
