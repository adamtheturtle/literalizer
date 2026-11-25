module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EDict [("items", EList [EInt 1, EDict [("value", EInt 2)]])]),
    ("second", EDict [("items", EList [EInt 1, EDict [("value", EInt 3)]])])
    ]
