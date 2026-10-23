module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("times", EList [EStr "09:30:00", EStr "17:45:00", EStr "23:59:59"])
    ]
