module Check exposing (..)


type Val
    = ENull
    | EInt Int
    | EStr String
    | EList (List Val)
    | EDict (List ( String, Val ))


my_data : Val
my_data = EDict [
    ("nil", EList (EList (EList (EList (EList (EList (EList (EList (EList (ENull :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("empty", EList (EList (EList (EList (EList (EList (EList (EList (EList (EList [] :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: [])),
    ("siblings", EList (EList (EList (EList (EList (EList (EList (EList (EList (EList [EInt 4, EInt 5] :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []) :: []))
    ]
