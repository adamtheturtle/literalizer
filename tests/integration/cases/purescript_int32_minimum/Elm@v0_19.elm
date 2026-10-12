module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("minimum", EInt (-2147483648)),
    ("neighbor", EInt (-2147483647)),
    ("maximum", EInt 2147483647),
    ("nested", EList [EInt (-2147483648)])
    ]
