module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("age", EInt 30),
    ("active", EBool True),
    ("score", ENull)
    ]
