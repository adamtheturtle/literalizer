module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EBool True,
    EStr "hi",
    EList [EInt 1, EInt 2],
    ENull
    ]
