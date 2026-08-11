module Main

type Val =
    | FInt of int64
    | FStr of string
    | FMap of (string * Val) list
let my_data: Val = FMap [
    ("assert", FInt 1L);
    ("else", FInt 1L);
    ("error", FInt 1L);
    ("false", FInt 1L);
    ("for", FInt 1L);
    ("function", FInt 1L);
    ("if", FInt 1L);
    ("import", FInt 1L);
    ("importbin", FInt 1L);
    ("importstr", FInt 1L);
    ("in", FInt 1L);
    ("local", FInt 1L);
    ("null", FInt 1L);
    ("self", FInt 1L);
    ("super", FInt 1L);
    ("tailstrict", FInt 1L);
    ("then", FInt 1L);
    ("true", FInt 1L);
    ("ordinary", FInt 1L)
]
