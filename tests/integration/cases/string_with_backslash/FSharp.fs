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

let x: Val = FList [
    FStr "C:\\path\\to\\file";
    FStr "back\\\\slash";
    FStr "hello \\\"world\\\""
]
