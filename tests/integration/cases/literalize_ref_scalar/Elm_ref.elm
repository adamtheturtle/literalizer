module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


myInt : Val
myInt = EInt 42
my_data : Val
my_data = myInt
