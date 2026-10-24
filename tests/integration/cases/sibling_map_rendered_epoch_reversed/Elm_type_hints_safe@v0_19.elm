module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("b", EDict [("k", EInt 1)]),
    ("a", EDict [("k", EStr "2040-01-01T00:00:00+00:00")])
    ]
