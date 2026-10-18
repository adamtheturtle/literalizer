module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [("k", EInt 2208988800)]),
    ("b", EDict [("k", EInt 1)])
    ]
