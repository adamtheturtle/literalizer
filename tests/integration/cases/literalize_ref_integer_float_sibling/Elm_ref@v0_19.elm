module Check exposing (..)


type Val
    = EInt Int
    | EFloat Float
    | EList (List Val)


integerValue : Val
integerValue = EFloat 1.0
my_data : Val
my_data = EList [
    integerValue,
    EFloat 1.5
    ]
