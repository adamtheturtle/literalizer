module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "1901-12-13T20:45:51",
    EStr "1901-12-13T20:45:52",
    EStr "2038-01-19T03:14:07",
    EStr "2038-01-19T03:14:08"
    ]
