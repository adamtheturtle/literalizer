module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EList [EDict [("name", EStr "Alice")], EDict [("name", EStr "Bob")]],
    EList [EDict [("name", EStr "Charlie")], EDict [("name", EStr "Dave")]]
    ]
