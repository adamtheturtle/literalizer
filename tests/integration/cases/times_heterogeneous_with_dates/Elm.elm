module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("vals", EList [EStr "2024-01-15", EStr "09:30:00"])
    ]
