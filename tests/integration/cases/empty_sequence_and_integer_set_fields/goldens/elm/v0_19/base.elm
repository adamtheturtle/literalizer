module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))
    | ESet (List Val)


my_data : Val
my_data = EDict [
    ("a", EList []),
    ("b", ESet [EInt 1, EInt 2])
    ]
