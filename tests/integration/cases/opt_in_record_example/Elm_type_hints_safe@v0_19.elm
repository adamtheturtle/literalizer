module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("name", EStr "Ada"),
    ("active", EBool True),
    ("scores", EList [EInt 1, EInt 2, EInt 3])
    ]
