module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("lint", EList [EInt 2, EList []]),
    ("test", EList [EInt 5, EList [EStr "compile"]])
    ]
