module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


shared : Val
shared = EList [
    EInt 1,
    EInt 2
    ]
my_data : Val
my_data = EList [
    shared,
    shared
    ]
