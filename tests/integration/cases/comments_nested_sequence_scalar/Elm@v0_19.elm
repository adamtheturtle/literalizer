module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [EStr "ADD", EStr "alice", EStr "hello"],
    EList [EStr "DEL", EStr "bob", EStr "5"]  -- removes "world"
    ]
