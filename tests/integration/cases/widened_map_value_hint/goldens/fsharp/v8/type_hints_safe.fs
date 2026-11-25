module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FList of Val list
    | FMap of (string * Val) list
let my_data: Val = FList [
    FMap [("a", FInt 1L)];
    FInt 1L;
    FStr "x";
    FBool true;
    FFloat 2.5;
    FNull
]
