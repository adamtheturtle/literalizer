module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("items", EList [EDict [("inner", EDict [("x", EInt 1)])], EDict [("inner", EDict [])]])],
    EDict [("items", EList [EDict [("inner", EDict [("x", EInt 2)])], EDict [("inner", EDict [])]])]
    ]
