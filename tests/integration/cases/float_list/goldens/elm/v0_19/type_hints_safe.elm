module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat 1.1,
    EFloat (-2.2),
    EFloat 3.3
    ]
