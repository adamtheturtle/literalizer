module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


x : Val
x = EList [
    EInt 1,
    EInt 2
    ]
my_data : Val
my_data = x
