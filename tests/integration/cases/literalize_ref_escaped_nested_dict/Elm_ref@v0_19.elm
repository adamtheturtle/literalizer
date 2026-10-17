module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


existing : Val
existing = EInt 1
my_data : Val
my_data = EDict [
    ("nested", EList [EInt 0, existing])
    ]
