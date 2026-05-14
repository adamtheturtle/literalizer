module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("0a", EStr "first"),
    ("1b", EStr "second")
    ]
