module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [("k", EStr "07:30:00")]),
    ("b", EDict [("k", EStr "string")])
    ]
