module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 1,
    EStr "a",
    EFloat 2.5
    ]
