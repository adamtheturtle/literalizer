module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


shared : Val
shared = EList [
    EInt 1,
    EStr "x"
    ]
my_data : Val
my_data = EList [
    shared,
    shared
    ]
