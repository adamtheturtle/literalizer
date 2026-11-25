module Check exposing (..)


type Val
    = JInt Int
    | JFloat Float
    | JList (List Val)


my_data : Val
my_data = JList [
    JInt (-42),
    JInt 0,
    JInt 42,
    JFloat (-1.25),
    JFloat 0.0,
    JFloat 1.25
    ]
