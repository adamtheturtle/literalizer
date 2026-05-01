module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_var : Val
my_var = EDict [
    ("_", EStr "_")
    ]
my_data : Val
my_data = my_var
