module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("scores", EDict [("1", EStr "first"), ("2", EStr "second")])
    ]
