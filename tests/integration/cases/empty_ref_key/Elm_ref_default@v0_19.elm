module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


external_value : Val
external_value = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EList [
    external_value
    ]
