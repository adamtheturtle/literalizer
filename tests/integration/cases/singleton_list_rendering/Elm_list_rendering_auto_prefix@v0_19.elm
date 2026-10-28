module Check exposing (..)


type Val
    = JInt Int
    | JList (List Val)


my_data : Val
my_data = JList (
    JInt 1
     :: [])
