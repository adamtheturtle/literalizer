module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EList (EInt 1 :: []),
    EList (EFloat 2.5 :: [])
    ]
