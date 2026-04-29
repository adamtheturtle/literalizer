module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


myVar : Val
myVar = EInt 0
my_data : Val
my_data = EDict [
    ("key", myVar)
    ]
