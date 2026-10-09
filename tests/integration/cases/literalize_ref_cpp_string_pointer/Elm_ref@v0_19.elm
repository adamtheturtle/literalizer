module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


shared : Val
shared = EStr "s"
my_data : Val
my_data = EDict [
    ("value", shared)
    ]
