module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


sharedVar : Val
sharedVar = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    sharedVar,
    sharedVar
    ]
