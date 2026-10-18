module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("minimum", EInt (-0x80000000)),
    ("below", EInt (-0xb2d05e00))
    ]
