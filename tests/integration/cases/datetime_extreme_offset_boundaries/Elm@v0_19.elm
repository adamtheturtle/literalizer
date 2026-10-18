module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "2020-06-15T12:00:00-23:59",
    EStr "2020-06-15T12:00:00-18:00",
    EStr "2020-06-15T12:00:00+18:00",
    EStr "2020-06-15T12:00:00+23:59"
    ]
