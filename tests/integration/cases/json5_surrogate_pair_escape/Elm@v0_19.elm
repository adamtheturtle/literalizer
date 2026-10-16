module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("astral", EStr "😀"),
    ("mixed", EStr "a😀b"),
    ("count", EInt 2),
    ("list", EList [EStr "😀", EInt 1]),
    ("nested", EDict [("inner", EStr "😀")])
    ]
