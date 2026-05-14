module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


deep : Val
deep = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = EDict [
    ("a", EDict [("b", EDict [("c", deep)])])
    ]
