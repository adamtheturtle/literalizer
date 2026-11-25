module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("call", EStr "send"),
    ("args", EList [EInt 1, EStr "email", EStr "a@gmail.com", EInt 100])
    ]
