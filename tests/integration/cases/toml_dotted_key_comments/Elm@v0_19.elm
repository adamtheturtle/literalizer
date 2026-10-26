module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- first dotted key
    -- second dotted key
    ("a", EDict [("b", EInt 1), ("c", EInt 2)])
    ]
