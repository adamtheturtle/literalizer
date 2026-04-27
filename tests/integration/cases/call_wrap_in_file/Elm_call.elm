module Check exposing (..)


process : ( a, b ) -> ()
process _ = ()
type Val
    = EInt Int
    | EList (List Val)


main : ()
main =
    let
        _ = process(EInt 1, EInt 2)
        _ = process(EInt 3, EInt 4)
    in
    ()
