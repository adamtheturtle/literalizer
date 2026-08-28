module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("first", EList [EInt 1, EInt 2]),
    ("second", EInt 3)  -- About the second key.
    ]
