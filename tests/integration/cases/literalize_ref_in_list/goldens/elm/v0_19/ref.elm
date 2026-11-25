module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


valX : Val
valX = EDict [
    ("_", EStr "_")
    ]
valY : Val
valY = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    valX,
    valY
    ]
