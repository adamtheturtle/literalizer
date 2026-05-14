module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EDict (List ( String, Val ))
    | ESet (List Val)


my_data : Val
my_data = EDict [
    ("name", EStr "Alice"),
    ("tags", ESet [
        EBool True,
        EInt 42,
        EStr "apple"
        ])
    ]
