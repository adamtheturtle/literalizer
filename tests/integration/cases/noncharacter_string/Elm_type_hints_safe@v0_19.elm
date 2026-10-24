module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("fffe", EStr "￾"),
    ("ffff", EStr "￿")
    ]
