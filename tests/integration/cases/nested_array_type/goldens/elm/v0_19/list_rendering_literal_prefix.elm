module Check exposing (..)


type Val
    = JInt Int
    | JList (List Val)


my_data : Val
my_data = JList [
    JList [JList [JInt 1]]
    ]
