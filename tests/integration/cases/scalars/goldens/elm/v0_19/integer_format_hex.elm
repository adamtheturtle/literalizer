module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EFloat Float
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EInt 0x2a,
    EFloat 3.14,
    EBool True,
    EBool False,
    EStr "hello \"world\""
    ]
