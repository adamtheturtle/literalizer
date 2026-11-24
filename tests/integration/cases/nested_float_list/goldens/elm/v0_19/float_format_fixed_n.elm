module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EFloat 1.500000, EFloat 2.500000],
    EList [EFloat 3.500000, EFloat 4.500000]
    ]
