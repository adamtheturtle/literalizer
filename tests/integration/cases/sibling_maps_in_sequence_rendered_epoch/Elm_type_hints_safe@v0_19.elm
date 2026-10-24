module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("k", EStr "2040-01-01T00:00:00+00:00")],
    EDict [("k", EInt 1)]
    ]
