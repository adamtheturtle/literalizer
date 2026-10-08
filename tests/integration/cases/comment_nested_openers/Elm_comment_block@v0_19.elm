module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    {- nested openers /* and {- remain -}
    ("x", EInt 1)
    ]
