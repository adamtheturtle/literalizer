module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EStr "x"),
    ("b", EStr "y")
    ]
