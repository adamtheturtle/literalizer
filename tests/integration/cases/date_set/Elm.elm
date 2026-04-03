module Check exposing (..)


type Val
    = EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EStr "2024-01-15",
    EStr "2024-06-01"
    ]
