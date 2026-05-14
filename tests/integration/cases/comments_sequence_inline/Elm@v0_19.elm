module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "a",  -- note a
    EStr "b"  -- note b
    ]
