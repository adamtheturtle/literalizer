module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("flow", EList [
        EInt 1,
        -- After the first element.
        EInt 2
        ]),
    -- Between the key and its value.
    ("gap", EInt 3),
    -- On the block scalar header.
    ("block", EStr "Text.\n"),
    ("nested", EList [
        EInt 1,
        EInt 1
        -- On the nested alias.
        ]),
    ("anchored", EInt 4),
    ("alias", EInt 4)
    -- On the alias.
    ]
