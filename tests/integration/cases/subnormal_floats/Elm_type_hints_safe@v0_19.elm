module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 5.0e-324,
    EFloat (-5.0e-324),
    EFloat 1.0e-310
    ]
