module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [("b", EDict [("c", EDict [("$ref", EStr "deep")])])])
    ]
