module Main

type Val =
    | FNull
    | FBool of bool
    | FInt of int64
    | FFloat of float
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateTime
    | FDatetime of System.DateTime
let my_data: Val = FMap [
    ("s", FStr "string");
    ("i", FInt 1L);
    ("f", FFloat 1.5);
    ("b", FBool true);
    ("n", FNull);
    ("d", FStr (string (System.DateOnly(2024, 1, 15))));
    ("dt", FStr (string (System.DateTime(2024, 1, 15, 12, 0, 0))));
    ("by", FStr "48656c6c6f")
]
