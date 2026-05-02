module Check exposing (..)


type Val
    = EStr String
    | EDict (List ( String, Val ))


my_var : Val
my_var = EInt 1
my_data : Val
my_data = my_var
