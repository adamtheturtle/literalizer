module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


shared : Val
shared = EList [
    EList [EInt 1]
    ]
my_data : Val
my_data = shared
