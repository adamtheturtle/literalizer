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

let my_data: Val = FSet [
    // before apple
    FStr "apple";
    FStr "banana"  // banana inline
    // trailing
]
