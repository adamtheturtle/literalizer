module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("minimum", EInt (-2147483648)),
    ("below", EInt (-3000000000))
    ]
