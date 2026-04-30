module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | ESet (List Val)


my_data : Val
my_data = EList [
    ESet [EStr "a", EStr "b"]
    ]
