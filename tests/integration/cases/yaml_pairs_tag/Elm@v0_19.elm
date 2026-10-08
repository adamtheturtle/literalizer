module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("first", EInt 1)],
    EDict [("repeated", EStr "a")],
    EDict [("repeated", EStr "b")]
    ]
