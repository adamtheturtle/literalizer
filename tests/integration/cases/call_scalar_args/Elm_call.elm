module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)


process(EStr "hello")
process(EInt 42)
process(EBool True)
