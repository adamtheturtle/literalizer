module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [("k", EStr "2020-01-01")]),
    ("b", EDict [("k", EStr "string")])
    ]
