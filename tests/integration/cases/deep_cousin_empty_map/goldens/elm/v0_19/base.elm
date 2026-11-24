module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("outer", EDict [("inner", EDict [("x", EInt 1)])])],
    EDict [("outer", EDict [("inner", EDict [])])]
    ]
