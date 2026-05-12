module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("sibling_lists", EDict [("numbers", EList [EInt 1, EInt 2]), ("strings", EList [EStr "x", EStr "y"])]),
    ("ref_marker_present", EList [EStr "$keep", EStr "z"])
    ]
