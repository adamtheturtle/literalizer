module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("scores", EList [EInt 10, EInt 20, EInt 30]),
    ("args", EList [EInt 1, EStr "email", EStr "a@gmail.com", EInt 100])
    ]
