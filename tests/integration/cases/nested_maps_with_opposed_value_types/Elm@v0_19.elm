module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("input", EDict [("name", EStr "alice"), ("city", EStr "paris")]), ("expected", EDict [("count", EInt 1), ("total", EInt 2)])],
    EDict [("input", EDict [("name", EInt 10), ("city", EInt 20)]), ("expected", EDict [("count", EStr "done"), ("total", EStr "pending")])]
    ]
