module Check exposing (..)


type Val
    = EBool Bool
    | EInt Int
    | EStr String
    | EList (List Val)
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process(EStr "hello")
        _ = process(EInt 42)
        _ = process(EBool True)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
