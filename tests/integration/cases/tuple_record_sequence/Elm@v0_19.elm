module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("call", EStr "send"), ("args", EList [EInt 1, EStr "email", EStr "a@gmail.com", EInt 100])],
    EDict [("call", EStr "recv"), ("args", EList [EInt 2, EStr "sms", EStr "b@example.com", EInt 200])]
    ]
