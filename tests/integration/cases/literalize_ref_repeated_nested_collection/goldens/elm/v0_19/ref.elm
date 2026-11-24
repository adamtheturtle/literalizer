module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


shared : Val
shared = EList [
    EList [EInt 1, EInt 2],
    EDict [("value", EInt 1)]
    ]
my_data : Val
my_data = EList [
    shared,
    shared
    ]
