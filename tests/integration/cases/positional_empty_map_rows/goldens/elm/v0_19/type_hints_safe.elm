module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EList [EList [EInt 1, EStr "value"], EList []]),
    ("second", EList [EList [], EList [EInt 2, EStr "other"]])
    ]
