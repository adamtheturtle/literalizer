module Check exposing (..)


type Val
    = EFloat Float
    | EList (List Val)


my_data : Val
my_data = EList [
    EFloat (1 / 0),
    EFloat (-(1 / 0)),
    EFloat (0 / 0)
    ]
