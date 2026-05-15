module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("host", EStr "it's here"),  -- a comment
    ("port", EInt 80)  -- another
    ]
