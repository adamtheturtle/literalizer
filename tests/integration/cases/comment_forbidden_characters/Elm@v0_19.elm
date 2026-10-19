module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("a", EInt 1),  -- tab	here and bidi <U+202E>after
    ("b", EInt 2)
    ]
