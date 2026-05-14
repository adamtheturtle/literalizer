module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "hello",
    EInt 42
    ]
