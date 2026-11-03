module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("lists", EList [EList (EInt 1 :: []), EList (EStr "x" :: []), EList []]),
    ("maps", EList [EDict [("x", EInt 1)], EDict [("x", EStr "s")]]),
    ("empties", EDict [("a", EList (EInt 1 :: [])), ("b", EList [])])
    ]
