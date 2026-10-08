module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("alpha", EList [EInt 2, EList []]),
    ("beta", EList [EInt 5, EList [EStr "x"]])
    ]
