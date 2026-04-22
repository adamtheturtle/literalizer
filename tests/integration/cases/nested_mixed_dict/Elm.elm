module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("outer", EDict [("a", EInt 1), ("b", EStr "x"), ("c", ENull)])
    ]
