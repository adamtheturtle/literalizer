module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("minimum", EInt (-0x80000000)),
    ("neighbor", EInt (-0x7fffffff)),
    ("maximum", EInt 0x7fffffff),
    ("nested", EList [EInt (-0x80000000)])
    ]
