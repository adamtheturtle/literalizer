module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    -- first
    EStr "a",
    -- second
    EStr "b"
    ]
