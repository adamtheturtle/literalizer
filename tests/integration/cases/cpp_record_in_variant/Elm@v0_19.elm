module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("h", EList [EInt 1, EStr "a", EList [EInt 2, EStr "b"], EDict [("k", EList [EBool True])]])
    ]
