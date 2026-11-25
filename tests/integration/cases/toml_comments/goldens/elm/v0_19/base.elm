module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- before
    ("answer", EInt 42),  -- inline
    ("plain", EStr "ok")
    -- trailing
    ]
