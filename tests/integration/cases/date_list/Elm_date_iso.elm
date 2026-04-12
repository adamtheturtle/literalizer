module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "2024-01-15",
    EStr "2024-02-20"
    ]
