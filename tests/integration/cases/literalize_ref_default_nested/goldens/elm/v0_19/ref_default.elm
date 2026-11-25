module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


item_var : Val
item_var = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EDict [
    ("items", EList [item_var, EDict [("fallback", EStr "value")]])
    ]
