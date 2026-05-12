module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("users", EList [EDict [("name", EStr "Bob"), ("tags", EList [EStr "admin", EStr "user"])], EDict [("name", EStr "Carol"), ("tags", EList [EStr "guest"])]])
    ]
