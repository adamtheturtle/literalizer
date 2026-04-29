module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


x : Val
x = EInt 0
y : Val
y = EInt 0
my_data : Val
my_data = EList [
    x,
    y
    ]
