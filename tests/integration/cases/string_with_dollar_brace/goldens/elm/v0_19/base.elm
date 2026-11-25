module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "prefix ${HOME} suffix",
    EStr "${interpolated}"
    ]
