module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("if", FInt 1L);
    ("then", FInt 2L);
    ("else", FInt 3L);
    ("let", FInt 4L);
    ("in", FInt 5L);
    ("using", FInt 6L);
    ("missing", FInt 7L);
    ("assert", FInt 8L);
    ("as", FInt 9L);
    ("Infinity", FInt 10L);
    ("NaN", FInt 11L);
    ("merge", FInt 12L);
    ("Some", FInt 13L);
    ("toMap", FInt 14L);
    ("forall", FInt 15L);
    ("with", FInt 16L);
    ("ordinary", FInt 17L)
]
