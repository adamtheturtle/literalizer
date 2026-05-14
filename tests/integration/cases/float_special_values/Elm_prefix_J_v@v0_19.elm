module Check exposing (..)


type Val
    = JFloat Float
    | JList (List Val)


my_data : Val
my_data = JList [
    JFloat (1 / 0),
    JFloat (-(1 / 0)),
    JFloat (0 / 0)
    ]
