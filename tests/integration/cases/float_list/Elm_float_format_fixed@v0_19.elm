module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 1.100000,
    EFloat (-2.200000),
    EFloat 3.300000
    ]
