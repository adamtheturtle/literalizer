module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


userObj : Val
userObj = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = userObj
