module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "100% done",
    EStr "%(name) is here"
    ]
