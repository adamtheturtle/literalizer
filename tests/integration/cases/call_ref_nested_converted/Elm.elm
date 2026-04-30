module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EList [EDict [("$ref", EStr "myVar")], EInt 42, EStr "static"]]
    ]
