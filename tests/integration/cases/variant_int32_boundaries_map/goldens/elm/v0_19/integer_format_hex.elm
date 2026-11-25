module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("below", EInt (-0x80000001)),
    ("minimum", EInt (-0x80000000)),
    ("above", EInt (-0x7fffffff)),
    ("nested", EList (EInt 0x0 :: []))
    ]
