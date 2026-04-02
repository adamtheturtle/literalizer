module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    -- line 1
    -- line 2
    EStr "a"
    ]
