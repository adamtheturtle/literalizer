module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("project", EStr "alpha"),
    ("lead_task", EDict [("id", EInt 100), ("description", EStr "first task"), ("is_done", EBool False), ("blocks", EList [EInt 102, EInt 103])])
    ]
