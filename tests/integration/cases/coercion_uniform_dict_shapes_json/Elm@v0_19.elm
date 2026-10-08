module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("type", EStr "create"), ("name", EStr "a")],
    EDict [("type", EStr "update"), ("name", EStr "b")]
    ]
