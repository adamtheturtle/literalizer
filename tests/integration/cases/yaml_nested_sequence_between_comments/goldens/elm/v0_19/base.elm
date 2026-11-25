module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [
        EDict [("item", EStr "existing")],
        EStr "kept"
        -- This comment trails the first pair.
        ],
    EList [EDict [("item", EStr "next")], EStr "also kept"],
    -- This comment describes the last pair.
    EList [EDict [("item", EStr "last")], EStr "kept too"]
    ]
