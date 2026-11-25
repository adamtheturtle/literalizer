module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("below", EList (EList (EList (EList (EList (EList (EList (EList (EInt 1 :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("boundary", EList (EList (EList (EList (EList (EList (EList (EList (EList (EInt 2 :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("multiple", EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EList (EInt 3 :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("text", EList (EList (EList (EList (EList (EList (EList (EList (EList (EStr "value" :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("boolean", EList (EList (EList (EList (EList (EList (EList (EList (EList (EBool True :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("float", EList (EList (EList (EList (EList (EList (EList (EList (EList (EFloat 1.5 :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []))
    ]
