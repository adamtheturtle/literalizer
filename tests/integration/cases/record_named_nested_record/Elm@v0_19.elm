module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("collection", EStr "alpha"),
    ("featured_entry", EDict [("id", EInt 100), ("label", EStr "first entry"), ("enabled", EBool False), ("related_ids", EList [EInt 102, EInt 103])])
    ]
