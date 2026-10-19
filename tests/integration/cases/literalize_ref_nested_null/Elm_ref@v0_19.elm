module Check exposing (..)


type Val
    = ENull
    | EList (List Val)


myNull : Val
myNull = ENull
my_data : Val
my_data = EList [
    myNull,
    ENull
    ]
