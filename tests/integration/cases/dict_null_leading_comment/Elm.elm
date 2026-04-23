module Check exposing (..)


type Val
    = ENull
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- comment
    ("name", EStr "Alice"),
    ("score", ENull)
    ]
