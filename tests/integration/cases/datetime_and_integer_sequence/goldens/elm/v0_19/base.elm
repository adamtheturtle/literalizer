module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "2000-01-01T01:02:03",
    EInt 1
    ]
