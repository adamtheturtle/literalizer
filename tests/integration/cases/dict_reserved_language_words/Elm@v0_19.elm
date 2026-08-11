module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("assert", EInt 1),
    ("else", EInt 1),
    ("error", EInt 1),
    ("false", EInt 1),
    ("for", EInt 1),
    ("function", EInt 1),
    ("if", EInt 1),
    ("import", EInt 1),
    ("importbin", EInt 1),
    ("importstr", EInt 1),
    ("in", EInt 1),
    ("local", EInt 1),
    ("null", EInt 1),
    ("self", EInt 1),
    ("super", EInt 1),
    ("tailstrict", EInt 1),
    ("then", EInt 1),
    ("true", EInt 1),
    ("ordinary", EInt 1)
    ]
