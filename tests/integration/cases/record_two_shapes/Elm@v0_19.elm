module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("user", EDict [("id", EInt 1), ("name", EStr "Alice")]),
    ("project", EDict [("title", EStr "report"), ("tags", EList [EStr "draft", EStr "urgent"])])
    ]
