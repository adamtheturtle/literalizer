module Main

type Val =
    | FBool of bool
    | FInt of bigint
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("quantity", FInt 1000000L);
    ("big", FInt 18446744073709551615I);
    ("ratio", FFloat 2.5);
    ("label", FStr "tag");
    ("ok", FBool true)
]
