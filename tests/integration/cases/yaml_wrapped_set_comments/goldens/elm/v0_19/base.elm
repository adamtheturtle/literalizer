module Check exposing (..)


type Val
    = EInt Int
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EInt 10,  -- comment for ten
    EInt 2  -- comment for two
    ]
