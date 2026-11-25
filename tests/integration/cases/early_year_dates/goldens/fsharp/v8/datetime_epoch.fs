module Main

type Val =
    | FStr of string
    | FMap of (string * Val) list
    | FDate of System.DateOnly
    | FInt of int64
let my_data: Val = FMap [
    ("date", FDate (System.DateOnly(99, 5, 27)));
    ("naive", FInt(-62135551800L));
    ("recent", FInt 1716804000L)
]
