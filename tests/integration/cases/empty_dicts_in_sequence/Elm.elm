module Check exposing (..)


type Val
    = EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [],
    EDict []
    ]
