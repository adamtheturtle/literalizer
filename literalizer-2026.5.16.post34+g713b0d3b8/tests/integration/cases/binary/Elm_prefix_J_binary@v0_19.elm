module Check exposing (..)


type Val
    = JStr String
    | JList (List Val)


my_data : Val
my_data = JList [
    JStr "48656c6c6f"
    ]
