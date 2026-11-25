module Check exposing (..)


type Val
    = EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EList [
    EDict [("nested", EDict [("times", EList (EStr "1900-01-01T00:00:00+00:00" :: []))])],
    EDict []
    ]
