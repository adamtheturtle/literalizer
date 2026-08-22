module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("item", EStr "existing")],
    -- This comment describes the next item.
    EDict [("item", EStr "next")]
    ]
