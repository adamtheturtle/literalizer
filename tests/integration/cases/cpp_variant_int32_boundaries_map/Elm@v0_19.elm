module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("below", EInt (-2147483649)),
    ("minimum", EInt (-2147483648)),
    ("above", EInt (-2147483647)),
    ("nested", EList (EInt 0 :: []))
    ]
