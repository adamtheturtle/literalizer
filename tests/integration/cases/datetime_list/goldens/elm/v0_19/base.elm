module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "2024-01-15T12:30:00.123456+00:00",
    EStr "2024-06-01T08:00:00+00:00"
    ]
