module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


whole : Val
whole = EList [
    EInt 1,
    EInt 2
    ]
my_data : Val
my_data = whole
