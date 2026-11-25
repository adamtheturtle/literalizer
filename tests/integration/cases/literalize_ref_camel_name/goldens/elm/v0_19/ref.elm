module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


myVar : Val
myVar = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = myVar
