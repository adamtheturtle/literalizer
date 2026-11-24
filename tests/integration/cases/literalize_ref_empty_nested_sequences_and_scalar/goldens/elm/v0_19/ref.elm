module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)


seed : Val
seed = EInt 1
my_data : Val
my_data = EList [
    EList [],
    EList (EList [] :: []),
    seed
    ]
