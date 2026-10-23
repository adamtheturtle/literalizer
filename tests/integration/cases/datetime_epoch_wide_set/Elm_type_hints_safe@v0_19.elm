module Check exposing (..)


type Val
    = EStr String
    | ESet (List Val)


my_data : Val
my_data = ESet [
    EStr "2099-06-15T08:30:00"
    ]
