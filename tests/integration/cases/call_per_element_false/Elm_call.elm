module Check exposing (..)


type Val
    = EInt Int
process : a -> ()
process _ = ()


main : ()
main =
    let
        _ = process(EInt 1)
    in
    ()
