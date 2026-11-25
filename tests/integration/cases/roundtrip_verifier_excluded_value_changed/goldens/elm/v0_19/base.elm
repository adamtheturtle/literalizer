module Check exposing (..)


type Val
    = EBool Bool
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("keep", EBool True),
    ("skip", EBool False)
    ]
