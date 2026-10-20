module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EList (List Val)


myValue : Val
myValue = EList [
    EInt 1,
    EInt 2
    ]
my_data : Val
my_data = myValue
