module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    -- About the first dotted key.
    -- About the second dotted key.
    ("dotted", EDict [("first", EInt 1), ("second", EInt 2)]),
    ("plain", EInt 3),  -- About the plain key.
    -- Inside the table.
    ("table", EDict [("inner", EInt 4)]),
    -- Before the first entry.
    -- Before the second entry.
    ("entries", EList [EDict [("name", EStr "one")], EDict [("name", EStr "two")]])
    ]
