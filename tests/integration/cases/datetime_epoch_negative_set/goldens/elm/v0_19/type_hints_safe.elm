module Check exposing (..)


type Val
    = EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EStr "1969-12-31T23:59:59+00:00"
    ]
