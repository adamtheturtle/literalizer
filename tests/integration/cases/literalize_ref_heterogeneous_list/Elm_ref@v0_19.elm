module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)


one : Val
one = EInt 1
two : Val
two = EStr "s"
my_data : Val
my_data = EList [
    one,
    two
    ]
