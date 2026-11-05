module Check exposing (..)


type Val
    = JFloat Float
    | JList (List Val)


my_data : Val
my_data = JList [
    JFloat 1.0e-09,
    JFloat (-1.0e-09)
    ]
