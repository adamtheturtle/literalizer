module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


my_data : Val
my_data = EList [
    EStr "This long string keeps its structural comma beyond the Fortran wrapping window without a safe split.",
    EInt 1
    ]
