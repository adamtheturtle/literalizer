module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EDict [
        ("b", EList [EInt 1]),
        -- Outdented from the sequence, so the inner mapping claims this.
        ("c", EInt 2)
        ]),
    -- Outdented from the inner mapping too, so the root claims this.
    ("d", EInt 3)
    ]
