module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("mixed", EList [EList [EStr "09:30:00"], EList []])
    ]
