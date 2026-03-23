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

let x: Val = FMap [
    ("name", FStr "Alice");
    ("age", FInt 30L);
    ("active", FBool true);
    ("score", FNull);
    ("joined", FStr (string (System.DateOnly(2024, 1, 15))));
    ("last_login", FStr (string (System.DateTime(2024, 1, 15, 12, 30, 0))));
    ("avatar", FStr "48656c6c6f")
]
