module Check exposing (..)


type Val
    = EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EStr "apple",
    EStr "banana",
    EStr "cherry"
    ]
