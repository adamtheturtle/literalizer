module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("level1", EDict [("level2", EDict [("level3", EDict [("level4", EDict [("value", EStr "deep"), ("items", EList [EStr "a", EStr "b"])])]), ("sibling", EInt 42)]), ("tags", EList [EDict [("name", EStr "tag1"), ("meta", EDict [("priority", EInt 1), ("labels", EList [EStr "x", EStr "y"])])]])])
    ]
