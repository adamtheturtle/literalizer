module Check exposing (..)


type JsonVal
    = EFloat Float
    | EList (List JsonVal)


my_data : JsonVal
my_data = EList [
    EFloat (1 / 0),
    EFloat (-(1 / 0)),
    EFloat (0 / 0)
    ]
