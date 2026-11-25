module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EList [],
    EList (EInt 1 :: []),
    EList [EInt 1, EInt 2],
    EList [EInt 1, EStr "x", EBool True, ENull],
    EList [EInt 1, EInt 2, EInt 3, EInt 4, EInt 5, EInt 6, EInt 7, EInt 8]
    ]
