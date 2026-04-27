module Check exposing (..)


type Val
    = EInt Int
    | EList (List Val)
process : ( a, b ) -> ()
process _ = ()


main : ()
main =
    let
        _ = process(EInt 1, EInt 42)
        _ = process(EInt 2, EInt 100)
    in
    ()
