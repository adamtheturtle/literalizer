module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 1.0e-09,
    EFloat (-1.0e-09)
    ]
