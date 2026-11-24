module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("del", EStr "ab"),
    ("nel", EStr "ab"),
    ("c1", EStr "ab")
    ]
