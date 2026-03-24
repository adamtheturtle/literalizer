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
    FInt 0b11110100001001000000L;
    FInt(-0b10011010010L);
    FInt 0b11111111L;
    FInt(-0b1010L)
]
