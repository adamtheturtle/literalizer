module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("groups", EList [EList [EDict [("id", EInt 1)]], EList [EDict [("id", EInt 2)]]])
    ]
