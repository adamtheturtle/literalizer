module Check exposing (..)


type Val
    = ENull
    | EBool Bool
    | EFloat Float
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EBool True,
    EFloat 1.5,
    ENull,
    EStr "2020-01-01",
    EStr "2020-01-01T00:00:00+00:00",
    EList []
    ]
