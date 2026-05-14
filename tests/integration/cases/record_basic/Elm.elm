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
    ("description", EStr "She said \"hello\", then waved"),
    ("is_done", EBool False),
    ("blocks", EList [EInt 1, EInt 2, EInt 3])
    ]
