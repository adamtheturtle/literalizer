module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


valX : Val
valY : Val
valX = EDict [
    ("_", EStr "_")
    ]
valY = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    valX,
    valY
    ]
