module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList (
    EStr "1960-01-01T00:00:00+00:00"
     :: [])
