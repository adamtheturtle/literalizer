module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("single_map", EList [EDict []]),
    ("single_list", EList [EList [EInt 1]]),
    ("single_deep", EList [EList [EList [EInt 2]]])
    ]
