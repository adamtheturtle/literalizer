module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EList [
        EInt 1,
        EInt 2,
        EInt 3
        ]),  -- inline a
    ("b", EInt 2)  -- inline b
    ]
