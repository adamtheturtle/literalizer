module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 0x1,
    EStr "email",
    EStr "a@gmail.com",
    EInt 0x64
    ]
