module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EInt 2, EStr "hello"],  -- trailing note
    -- next element
    EList [EInt 3, EStr "world"]
    ]
