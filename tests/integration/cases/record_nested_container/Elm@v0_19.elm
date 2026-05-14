module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("title", EStr "report"),
    ("tags", EList [EStr "draft", EStr "urgent", EStr "review"]),
    ("priority", EInt 2)
    ]
