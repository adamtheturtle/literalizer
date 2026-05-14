module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("score", ENull),
    ("age", EInt 30)
    ]
