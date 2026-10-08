module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


myTime : Val
myTime = EStr "01:02:03"
my_data : Val
my_data = EDict [
    ("x", myTime)
    ]
