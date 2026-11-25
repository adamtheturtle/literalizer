module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("numbers", EList [EInt 1, EInt 2]),
    ("nested", EDict [("inner", EList (EInt 3 :: []))]),
    ("mixed", EList [EInt 4, EStr "five"])
    ]
