module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("lower", EInt 3735928559),
    ("upper", EInt 31),
    ("negative", EInt (-16)),
    ("zero", EInt 0)
    ]
