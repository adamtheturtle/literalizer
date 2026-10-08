module Check exposing (..)


type Val
    = ENull
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [ENull],
    EList []
    ]
