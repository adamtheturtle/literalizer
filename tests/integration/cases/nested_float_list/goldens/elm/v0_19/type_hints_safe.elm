module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EFloat 1.5, EFloat 2.5],
    EList [EFloat 3.5, EFloat 4.5]
    ]
