module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EBool True,
    EInt 42,
    EStr "apple"
    ]
