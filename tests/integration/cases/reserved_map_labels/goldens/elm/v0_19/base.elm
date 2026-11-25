module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("if", EInt 1),
    ("then", EInt 2),
    ("else", EInt 3),
    ("let", EInt 4),
    ("in", EInt 5),
    ("using", EInt 6),
    ("missing", EInt 7),
    ("assert", EInt 8),
    ("as", EInt 9),
    ("Infinity", EInt 10),
    ("NaN", EInt 11),
    ("merge", EInt 12),
    ("Some", EInt 13),
    ("toMap", EInt 14),
    ("forall", EInt 15),
    ("with", EInt 16),
    ("ordinary", EInt 17)
    ]
