module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 0.000000001,
    EFloat (-0.000000001)
    ]
