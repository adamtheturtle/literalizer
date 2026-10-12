module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


shared : Val
shared = EList [
    EInt 1,
    EInt 2
    ]
my_data : Val
my_data = EList [
    EDict [("left", shared), ("right", shared)]
    ]
