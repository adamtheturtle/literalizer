module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


myVar : Val
myVar = EInt 1
my_data : Val
my_data = EDict [
    ("key", myVar)
    ]
