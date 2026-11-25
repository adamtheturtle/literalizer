module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1,
    EStr "hello",
    EBool True
    ]
