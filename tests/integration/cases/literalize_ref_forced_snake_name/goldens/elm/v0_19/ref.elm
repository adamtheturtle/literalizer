module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


user_obj : Val
user_obj = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = user_obj
