module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


foo : Val
foo = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EDict [
    ("mapping", EDict [("value", foo)]),
    ("items", EList [EDict [("other", EInt 1)], foo])
    ]
