module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1,
    EStr "hello",
    EBool True,
    ENull
    ]
