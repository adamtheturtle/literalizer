module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("rows", EList [EDict [("replacement", EInt (-1)), ("present", EInt 1)], EDict [("replacement", EInt 2), ("present", EInt 3)]])
    ]
