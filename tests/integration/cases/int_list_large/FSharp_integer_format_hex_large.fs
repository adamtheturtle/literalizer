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
    FInt 0xf4240L;
    FInt(-0x4d2L);
    FInt 0xffL;
    FInt(-0xaL)
]
