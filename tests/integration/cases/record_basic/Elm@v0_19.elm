module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("id", EInt 1),
    ("label", EStr "She said \"hello\", then waved"),
    ("enabled", EBool False),
    ("related_ids", EList [EInt 1, EInt 2, EInt 3])
    ]
