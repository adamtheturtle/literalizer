module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [
        -- inner note
        ("b", EInt 1)  -- inline b
        ]),
    ("list", EList [
        EInt 1,  -- first
        EInt 2  -- second
        ])
    ]
