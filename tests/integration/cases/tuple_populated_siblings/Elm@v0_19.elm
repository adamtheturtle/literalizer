module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EInt 1, EList (EInt 2 :: [])],
    EList [EInt 3, EList (EInt 4 :: [])]
    ]
