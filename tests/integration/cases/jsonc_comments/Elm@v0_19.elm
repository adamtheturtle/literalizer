module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("url", EStr "https://example.org/a/*b*/"),
    ("count", EInt 2)
    ]
