module Check exposing (..)


type Val
    = ENull
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", ENull),
    ("b", ENull)
    -- trailing
    ]
