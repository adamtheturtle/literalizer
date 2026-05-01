module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_var : Val
my_var = EDict [
    ("_", EStr "_")
    ]
item_var : Val
item_var = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EDict [
    ("key", my_var),
    ("items", EList [item_var, EDict [("fallback", EStr "value")]])
    ]
