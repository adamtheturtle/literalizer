module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EList (List Val)


myValue : Val
myValue = ENull
my_data : Val
my_data = myValue
