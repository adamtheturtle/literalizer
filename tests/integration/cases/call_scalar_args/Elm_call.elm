module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : ()
main =
    let
        _ = process(EStr "hello")
        _ = process(EInt 42)
        _ = process(EBool True)
    in
    ()
