module Check exposing (..)


type Val
    = EInt Int
    | EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        myVar : Val
        myVar = EInt 42
        _ = process(EList [myVar, EInt 42, EStr "static"])
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
