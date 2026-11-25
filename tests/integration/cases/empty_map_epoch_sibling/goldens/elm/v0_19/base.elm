module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("timestamp", EStr "2020-01-01T00:00:00+00:00")],
    EDict []
    ]
