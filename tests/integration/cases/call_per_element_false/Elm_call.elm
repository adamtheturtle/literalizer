module Check exposing (..)


type Val
    = EInt Int
process : a -> ()
process _ = ()


main : Program () () Never
main =
    let
        _ = process(EInt 1)
    in
    Platform.worker
        { init = \_ -> ( (), Cmd.none )
        , update = \_ m -> ( m, Cmd.none )
        , subscriptions = \_ -> Sub.none
        }
