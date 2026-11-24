module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("timestamp", EStr "2040-01-01T03:00:00+03:00")],
    EDict []
    ]
