module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList (
    EDict [("a\tb\nc", EInt 1), ("id", EStr "x")]
     :: [])
