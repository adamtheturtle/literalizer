module Check exposing (..)


type Val
    = JInt Int
    | JList (List Val)


my_data : Val
my_data = JList [
    JList (JInt 1 :: []),
    JList [],
    JList [JInt 2, JInt 3]
    ]
