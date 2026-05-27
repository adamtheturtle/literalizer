module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 0.000000,
    EFloat 1.000000,
    EFloat 1500.000000,
    EFloat 0.001000,
    EFloat 10000000000000000.000000
    ]
